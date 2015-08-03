"""
Abstraction layer over PagerDuty's contexts
"""


NOT_PROVIDED = object()


class PagerDutyContext(object):
    """
    PagerDuty context base class
    """
    TYPE_IMAGE = 'image'
    TYPE_LINK = 'link'

    type = NOT_PROVIDED
    href = NOT_PROVIDED
    src = NOT_PROVIDED
    text = NOT_PROVIDED
    alt = NOT_PROVIDED

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

        # TODO: If PagerDuty API is more forgiving, skip all that validation
        if self.type not in (self.TYPE_IMAGE, self.TYPE_LINK,):
            raise TypeError('Type of context must be either "image" or "link"')
        elif self.type == self.TYPE_IMAGE:
            # Image validation
            if self.src is NOT_PROVIDED:
                raise ValueError('Image context must have "src" provided')
            elif self.text is not NOT_PROVIDED:
                raise ValueError(
                    'Image context cannot have "text" attached to it',
                )
        elif self.type == self.TYPE_LINK:
            # Link validation
            if self.href is NOT_PROVIDED:
                raise ValueError('Link context must have "href" provided')
            elif self.src is not NOT_PROVIDED:
                raise ValueError(
                    'Link context cannot have "src" attached to it',
                )
            elif self.alt is not NOT_PROVIDED:
                raise ValueError(
                    'Image context cannot have "alt" attached to it',
                )

    def to_dict(self):
        """
        Transform current context into dictionary
        :return: context transformed into dictionary
        :rtype: dict
        """
        result = {
            'type': self.type,
        }
        if self.type == self.TYPE_IMAGE:
            result['src'] = self.src
            if self.href is not NOT_PROVIDED:
                result['href'] = self.href
            if self.alt is not NOT_PROVIDED:
                result['alt'] = self.alt
        elif self.type == self.TYPE_LINK:
            result['href'] = self.href
            if self.text is not NOT_PROVIDED:
                result['text'] = self.text
        else:
            raise NotImplementedError(
                '{} cannot be converted to dictionary'.format(
                    repr(self.__class__),
                ),
            )
        return result


class Image(PagerDutyContext):
    """
    Image PagerDuty context
    """
    type = 'image'


class Link(PagerDutyContext):
    """
    Link PagerDuty context
    """
    type = 'link'
