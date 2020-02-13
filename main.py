import re
from photo import Photo

def main():
    # read file
    with open("b_lovely_landscapes.txt", "r") as f:
        # read info
        number_of_photos = re.split("[ \n]", f.readline())[0]
        horizontal_photos = []
        vertical_photos = []
        code = 0
        while True:
            line = f.readline()
            if not line:
                break

            photo_info = re.split("[ \n]", line)
            orientation = photo_info[0]
            number_of_tags = photo_info[1]
            tags = set(photo_info[2:len(photo_info) - 1])
            photo = Photo(code, orientation, tags, number_of_tags)

            if orientation == 'H':
                horizontal_photos.append(photo)
            else:
                vertical_photos.append(photo)
            code += 1

        horizontal_photos.sort(key=lambda x: x.number_of_tags, reverse=False)

        slides = []
        photo = horizontal_photos.pop(0)
        slide = Slide(photo.tags,[photo])
        slides.append(slide)

        i = 0
        while horizontal_photos:
            print("i am in H", i)
            i += 1
            photo = horizontal_photos.pop(0)

            score_of_slides = []
            for slide in slides:
                score_of_slides.append(calc_score(slide.tags, photo.tags))
            max_value = max(score_of_slides)
            max_index = score_of_slides.index(max_value)
            max_slide = slides[max_index]

            # max slide on last slide
            if len(slides) == max_index + 1:
                slide = Slide(photo.tags, [photo])
                slides.append(slide)
            # max slide on first slide
            elif max_index == 0:
                slide = Slide(photo.tags, [photo])
                slides.insert(max_index, slide)
            # max slide on the middle
            else:
                left_slide = slides[max_index - 1]
                right_slide = slides[max_index + 1]
                if max_slide.is_better_neighbour_slide(right_slide.tags, photo.tags):
                    slide = Slide(photo.tags, [photo])
                    slides.insert(max_index + 1, slide)
                elif max_slide.is_better_neighbour_slide(left_slide.tags, photo.tags):
                    slide = Slide(photo.tags, [photo])
                    slides.insert(max_index - 1, slide)
                else:
                    slide = Slide(photo.tags, [photo])
                    slides.append(slide)






        while vertical_photos:
            print("I stuck in V")
            photo = vertical_photos.pop(0)
            score_of_slides = []
            for slide in slides :
                if (len(slide.photos) == 2) or slide.photos[0].orientation == 'H':
                    score_of_slides.append(calc_score(slide.tags, photo.tags))
                else:
                    score_of_slides.append(-1)

            max_value = max(score_of_slides)
            max_index = score_of_slides.index(max_value)
            max_slide = slides[max_index]

            # max slide on last slide
            if len(slides) == max_index + 1:
                left_slide = slides[max_index-1]
                if len(left_slide.photos) == 1 and left_slide.photos[0].orientation == 'V':
                    left_slide.photos.append(photo)
                    left_slide.tags = left_slide.tags | photo.tags
                elif len(left_slide.photos) == 2 or left_slide.photos[0].orientation == 'H':
                    slide = Slide(photo.tags, [photo])
                    slides.append(slide)
            # max slide on first slide
            elif max_index == 0:
                right_slide = slides[max_index+1]
                if len(right_slide.photos) == 1 and right_slide.photos[0].orientation == 'V':
                    right_slide.photos.append(photo)
                    right_slide.tags = right_slide.tags | photo.tags
                elif len(right_slide.photos) == 2 or right_slide.photos[0].orientation == 'H' :
                    slide = Slide(photo.tags, [photo])
                    slides.insert(max_index,slide)
            # max slide on the middle
            else:
                left_slide = slides[max_index - 1]
                right_slide = slides[max_index + 1]
                if len(left_slide.photos) == 1 and left_slide.photos[0].orientation == 'V':
                    left_slide.photos.append(photo)
                    left_slide.tags = left_slide.tags | photo.tags
                elif len(right_slide.photos) == 1 and right_slide.photos[0].orientation == 'V':
                    right_slide.photos.append(photo)
                    right_slide.tags = right_slide.tags | photo.tags
                else:
                    if max_slide.is_better_neighbour_slide(right_slide.tags,photo.tags):
                        slide = Slide(photo.tags, [photo])
                        slides.insert(max_index+1, slide)
                    elif max_slide.is_better_neighbour_slide(left_slide.tags,photo.tags):
                        slide = Slide(photo.tags, [photo])
                        slides.insert(max_index - 1, slide)
                    else:
                        slide = Slide(photo.tags, [photo])
                        slides.append(slide)

        for slide in slides:
            print([photo.code for photo in slide.photos])

        score = 0
        for i in range(len(slides)-1):
            score += calc_score(slides[i].tags,slides[i+1].tags)
        print(score)


class Slide(object):
    def __init__(self,tags,photos):
        self.tags = tags
        self.photos = photos

    def is_better_neighbour_slide(self,tags1, tags2):
        score1 = calc_score(tags1,self.tags)
        score2 = calc_score(tags2,self.tags)
        if score1 > score2:
            return False
        else:
            return True


def calc_score(tags1,tags2):
    return min(len(tags1 & tags2),len(tags1 - tags2), len(tags2 - tags1))

def calc_number_of_common_tags(x,y):
    return len(x & y)


def calc_number_of_different_tags(x,y):
    return len(x -y)


if __name__ == '__main__':
    main()