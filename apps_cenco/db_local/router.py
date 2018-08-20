
class Router(object):

    appname = 'db_local'
    db_name = 'local_settings'

    def db_for_read(self, model, **hints):
        """
        Attempts to read self.appname models go to model.db.
        """
        if model._meta.app_label == self.appname:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write self.appname models go to model.db.
        """
        if model._meta.app_label == self.appname:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the self.appname app is involved.
        """
        if obj1._meta.app_label == self.appname or \
           obj2._meta.app_label == self.appname:
            return True
        return None

    # This is possibly the new way, for beyond 1.8.
    ''' 
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the self.appname app only appears in the self.appname
        database.
        """
        if app_label == self.appname:
            return db == self.appname
        return None
    '''

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Example app's models get created on the right database."""
        if app_label == self.appname:
            # The Example app should be migrated only on the example_db database.
            return db == self.db_name
        elif db == self.db_name:
            # Ensure that all other apps don't get migrated on the example_db database.
            return False

        # No opinion for all other scenarios
        return None
