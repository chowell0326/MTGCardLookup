# MTG API CardData Lookup Script
# Author: Christian Howell
# Version: 1.09-610
# All Documentation for API and Documentation can be found at the following:
# Python SDK: https://github.com/MagicTheGathering/mtg-sdk-python?tab=readme-ov-file
# API Documentation: https://docs.magicthegathering.io/#documentationgetting_started

import os
from mtgsdk import Card, Set, Type, Supertype, Subtype, Changelog # type: ignore


class MTGCardLookup:
    def get_card_details_by_multiverseid(self, multiverseid):
        try:
            card = Card.find(multiverseid)
            if card:
                set_names = [self.get_set_name(code) for code in card.printings]
                card_details = {
                    "name": card.name,
                    "colors": card.colors,
                    "color_identity": card.color_identity,
                    "rarity": card.rarity,
                    "printed_sets": set_names,
                    "multiverseid": multiverseid
                }
                return card_details
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_set_name(self, set_code):
        try:
            mtg_set = Set.find(set_code)
            return mtg_set.name
        except Exception as e:
            print(f"An error occurred while fetching the set name: {e}")
            return set_code

    def format_to_markdown(self, card_details):
        if card_details:
            markdown_content = (
                f"# {card_details['name']}\n\n"
                f"**Colors**: {', '.join(card_details['colors']) if card_details['colors'] else 'None'}\n\n"
                f"**Color Identity**: {', '.join(card_details['color_identity']) if card_details['color_identity'] else 'None'}\n\n"
                f"**Rarity**: {card_details['rarity']}\n\n"
                f"**Printed Sets**: {', '.join(card_details['printed_sets'])}\n\n"
                f"**Multiverse ID**: {card_details['multiverseid']}\n\n"
            )
            return markdown_content
        else:
            return "# Card Not Found\n\nNo details available for the specified multiverseid."

    def save_markdown_to_file(self, markdown_content, output_path, author, version):
        if not output_path.endswith('.md'):
            output_path += '.md'
        try:
            with open(output_path, 'w') as file:
                file.write(markdown_content)
                file.write("MTG API Lookup - Version 1.0-610\n\u00A9Copyright Christian Howell 2024")
            print(f"Markdown file saved successfully at {output_path}")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")

    def process_export_command(self, multiverse_ids):
        markdown_content = ""
        for multiverseid in multiverse_ids:
            card_details = self.get_card_details_by_multiverseid(multiverseid)
            if card_details:
                markdown_content += self.format_to_markdown(card_details) + "\n\n"
            else:
                markdown_content += f"No card found with multiverseid {multiverseid}\n\n"

        output_path = input("Enter the output path for the Markdown file: ")
        author = "Christian Howell"
        version = "1.2-610"
        self.save_markdown_to_file(markdown_content, output_path, author, version)

if __name__ == "__main__":
    lookup = MTGCardLookup()
    multiverse_ids = []
    while True:
        user_input = input("Enter the multiverseid (or 'export' to quit and export): ")
        if user_input.lower() == 'export':
            if multiverse_ids:
                lookup.process_export_command(multiverse_ids)
            else:
                print("No multiverseids to export.")
            break
        try:
            multiverseid = int(user_input)
            multiverse_ids.append(multiverseid)
        except ValueError:
            print("Please enter a valid integer for the multiverseid.")
