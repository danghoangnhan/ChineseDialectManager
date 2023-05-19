from import_export.resources import logger


class BulkSaveMixin:
    """
    Overridden to store instance so that it can be imported in bulk.
    https://github.com/django-import-export/django-import-export/issues/939#issuecomment-509435531
    """
    bulk_instances = []

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        self.before_save_instance(instance, using_transactions, dry_run)
        if not using_transactions and dry_run:
            # we don't have transactions and we want to do a dry_run
            pass
        else:
            self.bulk_instances.append(instance)
        self.after_save_instance(instance, using_transactions, dry_run)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if self.bulk_instances:
            try:
                self._meta.model.objects.bulk_create(self.bulk_instances)
            except Exception as e:
                # Be careful with this
                # Any exceptions caught here will be raised.
                # However, if the raise_errors flag is False, then the exception will be
                # swallowed, and the row_results will look like the import was successful.
                # Setting raise_errors to True will mitigate this because the import process will
                # clearly fail.
                # To be completely correct, any errors here should update the result / row_results
                # accordingly.
                logger.error("caught exception during bulk_import: %s", str(e), exc_info=1)
                raise e
            finally:
                self.bulk_instances.clear()
