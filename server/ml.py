class Processing:
    def get_items_from_image(image):
        """
        Args
        -   image: idk like a 2D RGB tensor ??
        
        Returns list of cropped segmented 
        images of items (also 2D RGB tensors??) 
        from a single panoramic image. 
        """
        pass

    def filter_images(images: list):
        """
        removes irrelavant images from list of cropped images

        Returns: filtered list of cropped images
        """
        pass

    def get_image_vector_embedding(image):
        """
        Args
        - image: tensor of image

        Return
        - vector embedding tensor
        """
        pass

    def get_image_data(image):
        pass

    def get_image_list_data(list_of_images: list):
        """
        Given a list of images (tensors) returns a list of
        tuples where each tuple contains important data of the image

        returns Tuple[vectorEmbedding, name, desc, category]
        """
        pass

    def process_video(video):
        """
        Args
        - video: a video file of a room

        Return
        - String: response of successful video upload
        """
        pass