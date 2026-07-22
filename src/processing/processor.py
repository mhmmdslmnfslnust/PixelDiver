from processing.resizer import ImageResizer
from processing.grid_renderer import GridRenderer

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
        show_grid=False,
        cell_size=20,
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

        # Step 3 - Grid

        if show_grid:

            image = GridRenderer.render(
                image,
                cell_size=cell_size
            )

        return image