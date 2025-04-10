import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",   # Change this
        password="your_password",  # Change this
        database="blog_db"
    )

def create_post(title, content, tag_string):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        post_id = cursor.lastrowid

        tags = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
        for tag in tags:
            cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
            result = cursor.fetchone()
            if result:
                tag_id = result[0]
            else:
                cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))
                tag_id = cursor.lastrowid
            cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)", (post_id, tag_id))

        conn.commit()
        print("✅ Post created successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def view_all_posts():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT title FROM posts")
        posts = cursor.fetchall()
        print("\n📰 Blog Posts:")
        for post in posts:
            print(f"- {post[0]}")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def view_post_by_title(title):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT content FROM posts WHERE title = %s", (title,))
        result = cursor.fetchone()
        if result:
            print(f"\n📄 Content of '{title}':\n{result[0]}")
        else:
            print("❌ Post not found.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def search_posts_by_tag(tag_name):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = """
            SELECT p.title
            FROM posts p
            JOIN post_tags pt ON p.id = pt.post_id
            JOIN tags t ON pt.tag_id = t.id
            WHERE t.name = %s
        """
        cursor.execute(query, (tag_name,))
        posts = cursor.fetchall()
        if posts:
            print(f"\n📌 Posts with tag '{tag_name}':")
            for post in posts:
                print(f"- {post[0]}")
        else:
            print("❌ No posts found with that tag.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def main():
    while True:
        print("\n=== Blog CLI Menu ===")
        print("1. Create a new post")
        print("2. View all post titles")
        print("3. View a post by title")
        print("4. Search posts by tag")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            title = input("Enter post title: ")
            content = input("Enter post content: ")
            tags = input("Enter tags (comma-separated): ")
            create_post(title, content, tags)
        elif choice == '2':
            view_all_posts()
        elif choice == '3':
            title = input("Enter the post title: ")
            view_post_by_title(title)
        elif choice == '4':
            tag = input("Enter the tag: ")
            search_posts_by_tag(tag)
        elif choice == '5':
            print("👋 Exiting the blog CLI. Goodbye!")
            break
        else:
            print("❗ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
2