from functions.get_file_content import get_file_content
from config import MAX_CHARS


def test_lorem_truncation():
    content = get_file_content("calculator", "lorem.txt")

    assert len(content) > MAX_CHARS
    assert content.endswith(
        f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    )


if __name__ == "__main__":
    # Run truncation test
    test_lorem_truncation()
    print("Lorem truncation test passed ✅")

    # Additional test cases (print outputs)
    print("\n--- main.py ---")
    print(get_file_content("calculator", "main.py"))

    print("\n--- pkg/calculator.py ---")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\n--- /bin/cat (should error) ---")
    print(get_file_content("calculator", "/bin/cat"))

    print("\n--- pkg/does_not_exist.py (should error) ---")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))