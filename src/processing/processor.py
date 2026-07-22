from processing.resizer import ImageResizer


class ImageProcessor:
    """
    Central processing pipeline.

    Every future image operation will happen here.
    """

    @staticmethod
    def process(
        image,
        width,
        height,
        resize_method,
        palette=None,
        dithering=False,
    ):
        # Step 1 - Resize
        image = ImageResizer.resize(
            image,
            width,
            height,
            resize_method,
        )

        # Step 2 - Palette Reduction
        if palette is not None:
            from processing.quantizer import ColorQuantizer

            image = ColorQuantizer.quantize(
                image,
                palette,
                dithering,
            )

        return image