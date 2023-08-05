from data_slicer import plugin
from scipy.ndimage import gaussian_filter

class Example_Plugin(plugin.Plugin) :
    """ A barebones plugin which adds a single data blurring function to PIT.
    """

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        # It's a good idea to give the plugin a recognizable name
        self.name = 'Example plugin'
        # The shortname will be used as the variable name in the ipython 
        # console when plugins are autoloaded
        self.shortname = 'example'

    def blur(self, sigma=1) :
        """ Apply a Gaussian filter of standard deviation *sigma* to the 
        data, effectively blurring it out.

        .. Note::
            Successive calls to this function are additive. In order to get 
            rid of the blurring, use ``pit.reset_data()``.
        """
        # Get the data
        data = self.data_handler.get_data()
        # Set new data to the blurred out result
        self.data_handler.set_data(gaussian_filter(data, sigma))

    def example_function(self) :
        """ Just a simple example that shows how plugins print to the ipython 
        console.
        """
        print('This message is sent to you by the {}.'.format(self.name))

