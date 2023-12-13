import random
import webbrowser


# This function gets a list of keywords. Each keyword is right before the video id in a link:
# For example: https://youtu.be/UcaOpfwgyoM should have to youtu.be/ as a keyword.
def get_keywords(filename) -> list:
    with open(filename, 'r') as data:
        words = data.read()
        keywords = words.split('\n')  # Keywords should be separated in lines.

    return keywords


# This function extracts the id out of a link, with keyword as a check for that link.
# If the keyword is not found in the link, it just returns a blank string.
def extract_id_with_keyword(link, keyword) -> str:
    ID_LENGTH = 11  # Default id length on Youtube.
    keyword_length = len(keyword)
    keyword_index = link.find(keyword)

    # If keyword is not found in the link, return blank id.
    if keyword_index == -1:
        return ''

    start_index = keyword_index + keyword_length
    end_index = start_index + ID_LENGTH

    id = link[start_index:end_index]
    return id


# This function gets all the video ids in that file of links.
def get_video_ids(filename) -> list:
    video_ids = []
    keywords = get_keywords('Keywords.txt')

    with open(filename, 'r') as links:
        for link in links:
            for keyword in keywords:
                id = extract_id_with_keyword(link, keyword)

                # If id is a blank string, it is False in boolean.
                # If id is not a blank string, it is True in boolean and breaks the keyword loop.
                if id:
                    break
            video_ids.append(id)

    return video_ids


# This function puts all the video ids together separated by a comma for the final link.
def construct_youtube_link(video_ids) -> str:
    youtube_link = 'https://www.youtube.com/watch_videos?video_ids='

    # Append all ids.
    for id in video_ids:
        youtube_link += id + ','

    youtube_link = youtube_link[:-1]  # Remove the last comma.
    return youtube_link


# This function shuffles a list of items by the following:
#     - num_of_items is the number of items of each contributor.
#     - num_of_last_items is the number of items that should be at the final of the list for each contributor.
#     - That means that if we have 3 people, A, B and C. Each of them includes 5 items. When we set
#       num_of_last_items to 2, we should have the last 6 items to be 2 for A, 2 for B, 2 for C, randomly.
def calculated_shuffle(item_list, num_of_items, num_of_last_items) -> list:
    removed_item_list = []
    num_of_items_removed = 0  # This variable keeps tracks of how many items have been removed.

    # This iteration is for each and every contributor there is in the list.
    for i in range(0, len(item_list), num_of_items):
        # This iteration random gets <num_of_last_items> items out of the original list, without error, I hope.
        for j in range(0, num_of_last_items):
            # This variable decides the position to remove an item. That item will be put into the removed list.
            random_item_pos = i + random.randint(0, num_of_items - 1 - j) - num_of_items_removed
            removed_item = item_list.pop(random_item_pos)
            removed_item_list.append(removed_item)

        num_of_items_removed += num_of_last_items

    # Shuffle the truncated list and the removed list, then put the removed at the end of the truncated.
    random.shuffle(item_list)
    random.shuffle(removed_item_list)
    item_list.extend(removed_item_list)
    return item_list


# This function gets the arguments in the terminal interface.
# If there's only 2 arguments, the final argument will be added, which is 1.
def get_sys_args(sys_args) -> list:
    if len(sys_args) == 2:
        return sys_args[1:].append('1')
    if len(sys_args) == 3:
        return sys_args[1:]


if __name__ == '__main__':
    # Instruction of parameters.
    args = input('The parameter goes as follow:\n'
                 '- Number of items per contributor.\n'
                 '- Number of last item to keep the contributors listening.\n'
                 'Enter the numbers (space separation is fine): ')
    # Get all the arguments in the terminal interface.
    args = args.split(',')
    num_of_items_per_contributor, last_item_per_contributor = int(args[0]), int(args[1])

    # Extract video ids from the file.
    video_ids = get_video_ids('List_of_vids.txt')

    # Shuffle them up in a peculiar fashion and get the youtube link.
    video_ids = calculated_shuffle(video_ids, num_of_items_per_contributor, last_item_per_contributor)
    youtube_link = construct_youtube_link(video_ids)
    webbrowser.open(youtube_link)
