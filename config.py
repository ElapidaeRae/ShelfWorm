from manage import random_string


# Set the stripe keys for the stripe API which will be used to process payments
stripe_keys = {
    'secret_key': 'sk_test_51Op9XlE2jtOUNONEf2P66ve76ceV6d9FvtktJ1rs9RCz8akbbq5d5NrAXTXRvSaIMrxEdHyjUU9DGr8bIMa6JOwK00GJMVGAzW',
    'publishable_key': 'pk_test_51Op9XlE2jtOUNONEOkQeFgqjR8oDRMcTbEUprOoV4VI8pkdF3w5tDadoddWpDD7zqrXZsS3EqADlZEskGDtsYMyO00rhsJca7Z'
}

# Set the secret key to some random bytes. For production, a random key should be used
secret_key = 'According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don\'t care what humans think is impossible.'

# Set the recaptcha parameters
RECAPTCHA_PARAMETERS = {'hl': 'en', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
RECAPTCHA_PUBLIC_KEY = random_string(40)
RECAPTCHA_PRIVATE_KEY = random_string(40)

# The image parameters
images = ['jpg', 'jpeg', 'png', 'bmp']
image_max_size = 1024 * 1024 * 5