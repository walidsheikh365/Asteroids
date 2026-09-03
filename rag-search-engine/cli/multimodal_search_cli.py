import argparse

from multimodal_search import MultimodalSearch, verify_image_embedding, image_search_command

def main():
    parser = argparse.ArgumentParser(description="Multimodal Search CLI")

    subparsers = parser.add_subparsers(dest="command")
    
    verify_parser = subparsers.add_parser("verify_image_embedding", help="Verify image embedding")
    verify_parser.add_argument("image", type=str, help="Path to the image file")

    search_parser = subparsers.add_parser("image_search", help="Search with an image")
    search_parser.add_argument("image", type=str, help="Path to the image file")
    search_parser.add_argument("--top_k", type=int, default=5, help="Number of top results to return")


    args = parser.parse_args()

    model = MultimodalSearch()
    if args.command == "verify_image_embedding":
        verify_image_embedding(model, args.image)
    elif args.command == "image_search":
        image_search_command(model, args.image, top_k=args.top_k)

if __name__ == "__main__":
    main()