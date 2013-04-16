import logging
from Products.CMFCore.utils import getToolByName
# The profile id of your package:
PROFILE_ID = 'profile-collective.gavisits:default'


logger = logging.getLogger('collective.gavisits')


def add_catalog_indexes(context):
    """Add needed catalog indexes to the catalog
    taken from: http://maurits.vanrees.org/weblog/archive/2009/12/catalog
    """

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it
    # is quite safe.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()

    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('visits', 'FieldIndex'),)
    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def setupVarious(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('collective.gavisits-default.txt') is None:
        return
    portal = context.getSite()
    add_catalog_indexes(portal)
