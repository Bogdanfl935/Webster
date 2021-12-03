import os


# Scanned directory names
ROOT_DIR = 'templates'
TEMPLATES_INCLUDE_DIR = 'include'
TEMPLATES_INDIVIDUAL_DIR = 'individual'
TEMPLATES_LAYOUT_DIR = 'layout'
TEMPLATES_MODAL_DIR = 'modal'
TEMPLATES_SECTION_DIR = 'section'

# Scanned file names
INCLUDE_BOOTSTRAP_INCLUDES_FILE = 'bootstrap-includes.html'
INCLUDE_MATERIAL_DESIGN_INCLUDES_FILE = 'material-design-includes.html'
INDIVIDUAL_ERROR_FILE = 'error.html'
LAYOUT_BASE_FILE = 'base.html'
LAYOUT_LAYOUT_FILE = 'layout.html'
MODAL_BAD_TOKEN_FILE = 'bad-token.html'
MODAL_CONFIRM_FILE = 'confirm.html'
MODAL_LOGIN_FILE = 'login.html'
MODAL_MULTI_CHOICE_FILE = 'multi-choice.html'
MODAL_PASSWORD_RESET_FILE = 'password-reset.html'
SECTION_CRAWLED_CONTENT_FILE = 'crawled_content.html'
SECTION_HOME_FILE = 'home.html'

# Scanned file paths
INCLUDE_BOOTSTRAP_INCLUDES_PATH = '/'.join((TEMPLATES_INCLUDE_DIR, INCLUDE_BOOTSTRAP_INCLUDES_FILE))
INCLUDE_MATERIAL_DESIGN_INCLUDES_PATH = '/'.join((TEMPLATES_INCLUDE_DIR, INCLUDE_MATERIAL_DESIGN_INCLUDES_FILE))
INDIVIDUAL_ERROR_PATH = '/'.join((TEMPLATES_INDIVIDUAL_DIR, INDIVIDUAL_ERROR_FILE))
LAYOUT_BASE_PATH = '/'.join((TEMPLATES_LAYOUT_DIR, LAYOUT_BASE_FILE))
LAYOUT_LAYOUT_PATH = '/'.join((TEMPLATES_LAYOUT_DIR, LAYOUT_LAYOUT_FILE))
MODAL_BAD_TOKEN_PATH = '/'.join((TEMPLATES_MODAL_DIR, MODAL_BAD_TOKEN_FILE))
MODAL_CONFIRM_PATH = '/'.join((TEMPLATES_MODAL_DIR, MODAL_CONFIRM_FILE))
MODAL_LOGIN_PATH = '/'.join((TEMPLATES_MODAL_DIR, MODAL_LOGIN_FILE))
MODAL_MULTI_CHOICE_PATH = '/'.join((TEMPLATES_MODAL_DIR, MODAL_MULTI_CHOICE_FILE))
MODAL_PASSWORD_RESET_PATH = '/'.join((TEMPLATES_MODAL_DIR, MODAL_PASSWORD_RESET_FILE))
SECTION_CRAWLED_CONTENT_PATH = '/'.join((TEMPLATES_SECTION_DIR, SECTION_CRAWLED_CONTENT_FILE))
SECTION_HOME_PATH = '/'.join((TEMPLATES_SECTION_DIR, SECTION_HOME_FILE))

