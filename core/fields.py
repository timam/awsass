import uuid
from sorl.thumbnail import ImageField


class TimestampImageField(ImageField):

    def generate_filename(self, instance, filename):
        """Add timestamp at beginning of the file"""
        # Adding a timestamp at the beginning of the file name
        new_filename = "{}_{}".format(uuid.uuid4().hex, filename)
        filename = super(TimestampImageField, self).generate_filename(
            instance, new_filename)
        return filename
