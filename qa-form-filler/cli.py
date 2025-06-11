import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Automated QA Form Filler")
    
    parser.add_argument(
        "--login",
        action="store_true",
        help="Run login authentication before filling forms"
    )
    parser.add_argument(
        "--auth",
        type=str,
        help="Path to auth file (optional)"
    )
    parser.add_argument(
        "--urls",
        type=str,
        default="url_list.json",
        help="Path to JSON file containing list of URLs to test"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Attempt to submit the form after filling"
    )
    parser.add_argument(
        "--selenium",
        action="store_true",
        help="Use Selenium instead of Playwright"
    )

    return parser.parse_args()
