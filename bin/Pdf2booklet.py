from utils import *

dir = 'tmp'  # Needs input from config files
parent_dir = getcwd()


# Constraint image dimensions to page
def dim_constraint(image_size, paper_size):
    RATIO = image_size[WIDTH] / image_size[HEIGHT]
    PAPER_SIZE = SIZE[paper_size]  # width / height
    return (int(PAPER_SIZE[WIDTH] / 2), int((PAPER_SIZE[WIDTH] / 2) / RATIO))


# Create and return document structure as lists
def get_docstruct(NO_OF_PAGES, SPLIT_INTO_SETS=2):

    PAGE_ORDER = []
    for count in range(1, int(NO_OF_PAGES / SPLIT_INTO_SETS) + 1):
        PAGE_ORDER.append([])

    for index, PAGE in list(enumerate(PAGE_ORDER)):
        PAGE.append(list(x for x in range(
            index + 1, NO_OF_PAGES + 1, len(PAGE_ORDER))))
        [_PAGE] = PAGE
        PAGE_ORDER[index] = _PAGE
        _PAGE_ORDER = map(stringify, PAGE_ORDER)
    return _PAGE_ORDER, PAGE_ORDER


# Saving pages in jpeg format
def split_images(PDF_FILE, DPI):

    chdir(parent_dir)
    if path.exists(dir):
        rmtree(dir)

    makedirs(dir)

    PAGES = convert_from_path(
        PDF_FILE, DPI, poppler_path=R'poppler-21.08.0\Library\bin')
    chdir(dir)
    for index, page in enumerate(PAGES):
        page.save(str(index + 1) + '.jpg', 'JPEG')
    chdir(parent_dir)
    return PAGES.__len__()


# images edited into a single page
def combine_images(IMG1: str, IMG2: str, PAGE_SIZE: str = 'A4'):
    # Read the two images
    image1 = Image.open(IMG1)
    image2 = Image.open(IMG2)
    # resize, first image
    image1 = image1.resize(dim_constraint(image1.size, PAGE_SIZE))
    image2 = image2.resize(dim_constraint(image2.size, PAGE_SIZE))
    image1_size = image1.size
    new_image = Image.new('RGB', SIZE[PAGE_SIZE], (250, 250, 250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    file_name = generate_name(IMG1, IMG2)
    new_image.save(file_name, "JPEG")
    return file_name


# images to pages PDF
# PDF to doc (! optional)

def main_function(PDF_FILE: str, SAVE_PATH: str, PAGE_SIZE: str, DPI: int):
    chdir(parent_dir)
    # Load document and split pages
    NO_OF_PAGES = split_images(PDF_FILE, DPI)
    NAME_STRUCT, NUM_STRUCT = get_docstruct(NO_OF_PAGES)
    NAME_STRUCT, NUM_STRUCT = map(list, (NAME_STRUCT, NUM_STRUCT))
    COMBINED_list = []
    # Load and combine pages
    chdir(dir)

    for pages in NAME_STRUCT:
        thread1 = pool.apply_async(
            lambda *args: Image.open(combine_images(pages[0], pages[1], PAGE_SIZE)), (8,))
        COMBINED_list.append(thread1.get())
    newpdf_name = "OUT_B00kified.pdf"
    COMBINED_list[0].save(newpdf_name, "PDF", resolution=100.0,
                          save_all=True, append_images=COMBINED_list[1:])
    copy2(newpdf_name, SAVE_PATH + ".pdf")
    chdir(parent_dir)


if __name__ == '__main__':
    try:
        chdir(parent_dir)
        root = tk.Tk()
        app = App(root, main_function)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", "Unexpected Error : " + e)
    finally:
        exit()
