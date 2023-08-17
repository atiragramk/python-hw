import psycopg2
import psycopg2.extras
import psycopg2.errors
import uuid
import random
from datetime import datetime
import os


names = ['Katlyn', 'Lorri', 'Elaine', 'John', 'Valerie', 'Terri']
user_type = ['Host', 'Guest']


def main():
    psycopg2.extras.register_uuid()
    conn = psycopg2.connect(
        f"dbname={os.getenv('DB_NAME')} user={os.getenv('USER')}")
    cur = conn.cursor()

    # cur.execute("CREATE TYPE user_enum AS ENUM ('Host', 'Guest')")
    # cur.execute("CREATE TYPE payment_enum AS ENUM ('full', 'part')")

    cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                id uuid PRIMARY KEY,
                username varchar(50) NOT NULL,
                email varchar(50) NOT NULL,
                user_type user_enum NOT NULL
                )
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                id uuid PRIMARY KEY,
                host_id uuid NOT NULL,
                room_type varchar(50) NOT NULL,
                price int NOT NULL,
                capacity int NOT NULL,
                availability boolean NOT NULL,
                picture text[] NOT NULL,
                amenities varchar(100)[] NOT NULL,

                FOREIGN KEY (host_id)
                    REFERENCES users (id)
                )
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                id uuid PRIMARY KEY,
                guest_id uuid NOT NULL,
                room_id uuid NOT NULL,
                check_in_date timestamp NOT NULL,
                check_out_date timestamp NOT NULL,
                payment_status varchar(50) NOT NULL,
                number_of_guests int NOT NULL,
                total_price int NOT NULL,

                FOREIGN KEY (guest_id)
                    REFERENCES users (id),
                FOREIGN KEY (room_id)
                    REFERENCES rooms (id)
                )
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                id uuid PRIMARY KEY,
                guest_id uuid NOT NULL,
                reservation_id uuid NOT NULL,
                payment_amount int NOT NULL,
                payment_date timestamp NOT NULL,
                payment_method payment_enum NOT NULL,

                FOREIGN KEY (guest_id)
                    REFERENCES users (id),
                FOREIGN KEY (reservation_id)
                    REFERENCES reservations (id)
                )
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                id uuid PRIMARY KEY,
                guest_id uuid NOT NULL,
                room_id uuid NOT NULL,
                rating int NOT NULL,
                comment text NOT NULL,
                date_posted date NOT NULL,

                FOREIGN KEY (guest_id)
                    REFERENCES users (id),
                FOREIGN KEY (room_id)
                    REFERENCES rooms (id)
                )
                """)

    def create_users():
        for i in range(3):
            name = random.choice(names)
            cur.execute("""
                        INSERT INTO users (id, username, email, user_type) 
                        VALUES (%s, %s, %s,%s)""",
                        (uuid.uuid4(), name,
                         f'{name}{i}@gmail.com', random.choice(user_type))
                        )
    create_users()

    def create_rooms(host: str, type: str, price: int, capacity: int, availability: bool):
        photo = ['https://a0.muscache.com/im/pictures/dffbf405-6530-4660-a7f0-b1c9a1931a02.jpg?im_w=1200',
                 'https://a0.muscache.com/im/pictures/943b83b0-2abf-4dcf-ba7c-a6c2eb429dda.jpg?im_w=720']
        amenities = ['WiFi', 'Smart locks', 'Pet-friendly',
                     'A fully equipped kitchen', 'Hot tub', 'jacuzzi', 'Free parking']
        cur.execute("""
                    INSERT INTO rooms (
                    id,
                    host_id,
                    room_type,
                    price,
                    capacity,
                    availability,
                    picture,
                    amenities
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (uuid.uuid4(), host, type, price,
                     capacity, availability, photo, amenities)
                    )
        conn.commit()

    create_rooms(host='f5f55628-3cc3-11ee-a93c-089798a4699f',
                 type='apartment', price=120, capacity=2, availability=True)
    create_rooms(host='f5f54f77-3cc3-11ee-bb6e-089798a4699f',
                 type='house', price=55, capacity=2, availability=True)
    create_rooms(host='45c81ca6-f59c-4622-9e12-e545fd85fb80',
                 type='apartment', price=81, capacity=2, availability=True)

    def create_reservation(guest: str, room: str, date_in: str, date_out: str, status: str, number_guests: int):
        dt_in = datetime.strptime(date_in, "%Y/%m/%d")
        dt_out = datetime.strptime(date_out, "%Y/%m/%d")
        cur.execute(f"""
                    SELECT price 
                    FROM rooms
                    WHERE id='{room}'
                    """)
        delta = dt_out - dt_in
        delta.days
        price, = cur.fetchone()

        cur.execute("""
                    INSERT INTO reservations (
                    id,
                    guest_id,
                    room_id,
                    check_in_date,
                    check_out_date,
                    payment_status,
                    number_of_guests,
                    total_price
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (uuid.uuid4(), guest, room, dt_in,
                     dt_out, status, number_guests, price*delta.days)
                    )

    create_reservation(guest='94322ff9-3cc4-11ee-918c-089798a4699f',
                       room='09210b1f-ea33-464a-9e4d-077b13373ccd', date_in="2023/08/10", date_out="2023/08/16", status='pending', number_guests=2)
    create_reservation(guest='94322ff9-3cc4-11ee-918c-089798a4699f',
                       room='2ce5a0f2-8876-471c-9d2d-89b904459ad6', date_in="2023/08/14", date_out="2023/08/16", status='pending', number_guests=3)

    def create_payment(reservation: str, payment_date: str, method: str):
        dt_payment = datetime.strptime(payment_date, "%Y/%m/%d")
        cur.execute(f"""
                    SELECT guest_id, total_price
                    FROM reservations
                    WHERE id='{reservation}'
                    """)
        guest_id, total_price = cur.fetchone()

        try:
            cur.execute("""
                        INSERT INTO payments (
                        id,
                        guest_id,
                        reservation_id,
                        payment_amount,
                        payment_date,
                        payment_method
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (uuid.uuid4(), guest_id, reservation,
                            total_price, dt_payment, method)
                        )
            conn.commit()
            cur.execute(f"""
                        UPDATE reservations
                        SET payment_status = 'success'
                        WHERE id = '{reservation}'
                        """
                        )
            conn.commit()

        except psycopg2.errors:
            print(psycopg2.errors)

    def create_review(reservation: str, rating: int, review: str, date: int):
        dt_post = datetime.strptime(date, "%Y/%m/%d")
        cur.execute(f"""
                    SELECT guest_id, room_id
                    FROM reservations
                    WHERE id='{reservation}'
                    AND payment_status = 'success'
                    """)
        guest_id, room_id = cur.fetchone()

        try:
            cur.execute("""
                        INSERT INTO reviews (
                        id,
                        guest_id,
                        room_id,
                        rating,
                        comment,
                        date_posted
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (uuid.uuid4(), guest_id, room_id, rating, review, dt_post)
                        )
            conn.commit()

        except psycopg2.errors:
            print(psycopg2.errors)

    create_payment(reservation='184dbbe1-4efc-4781-a159-001698ed633a',
                   payment_date='2023/08/14', method='full')
    create_payment(reservation='644bf536-dd9d-40b6-ae41-794e315caf4b',
                   payment_date='2023/08/10', method='part')
    create_payment(reservation='6fbe4d7e-d3c1-430e-850b-5b6898c7ca76',
                   payment_date='2023/08/16', method='full')

    create_review(reservation='184dbbe1-4efc-4781-a159-001698ed633a',
                  review='Good apartment', rating=3, date='2023/08/16')
    create_review(reservation='644bf536-dd9d-40b6-ae41-794e315caf4b',
                  review='Great place for family rest', rating=2, date='2023/08/10')
    create_review(reservation='6fbe4d7e-d3c1-430e-850b-5b6898c7ca76',
                  review='Noisy neighbors', rating=4, date='2023/08/10')

    def get_user_biggest_amount_reservations():
        cur.execute("""
                    SELECT u.id, u.username, COUNT(r.id) AS num_reservations
                    FROM users u
                    JOIN reservations r ON u.id = r.guest_id
                    GROUP BY u.id, u.username
                    ORDER BY num_reservations DESC
                    LIMIT 1;
                    """)
        id, username, amount_reservations = cur.fetchone()
        return f'User ID: {id}, UserName: {username}'

    def get_user_biggest_earning():
        cur.execute("""
                    SELECT u.id, u.username, SUM(p.payment_amount) AS earnings
                    FROM users u
                    JOIN rooms r ON u.id = r.host_id
                    JOIN reservations res ON r.id = res.room_id
                    JOIN payments p ON res.id = p.reservation_id
                    WHERE EXTRACT(MONTH FROM p.payment_date) = EXTRACT (MONTH FROM CURRENT_DATE)
                    AND EXTRACT(YEAR FROM p.payment_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                    GROUP BY u.id, u.username
                    ORDER BY earnings DESC
                    LIMIT 1;
                    """)
        id, username, earnings = cur.fetchone()
        return f'User ID: {id}, UserName: {username}'

    def get_user_biggest_avg_rating():
        cur.execute("""
                    SELECT u.id, u.username, AVG(rev.rating) AS feedback
                    FROM users u
                    JOIN rooms r ON u.id = r.host_id
                    JOIN reviews rev ON r.id = rev.room_id
                    GROUP BY u.id, u.username
                    ORDER BY feedback DESC
                    LIMIT 1;
                    """)
        id, username, rating = cur.fetchone()
        return f'User ID: {id}, UserName: {username}'

    print(get_user_biggest_amount_reservations())
    print(get_user_biggest_earning())
    print(get_user_biggest_avg_rating())

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
