"""Reporting is derived from transactional records and has no persisted models.

Keeping reports as queries avoids duplicated financial and inventory data, and makes
every report reflect the current source-of-truth records.
"""
