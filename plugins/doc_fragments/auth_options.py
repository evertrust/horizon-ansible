class ModuleDocFragment(object):
    DOCUMENTATION = r'''
    options:
      x_api_id:
        description:
          - Horizon identifiant
        required: false
        type: str
      x_api_key:
        description:
          - Horizon password
        required: false
        type: str
      ca_bundle:
        description:
          - The location of a CA Bundle to use when validating SSL certificates.
        required: false
        type: str
      client_cert:
        description:
          - The location of a client side certificate.
        required: false
        type: str
      client_key:
        description:
          - The location of a client side certificate's key.
        required: false
        type: str
      endpoint:
        description:
          - url of the API
        required: true
        type: str
    '''
