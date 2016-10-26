#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related transactions derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


class ContributionBase(models.Model):
    """
    Abstract base model for contributions received or made, as itemized on
    Schedules A and C of Form 460.

    Records are derived from the RCPT_CD table.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        null=False,
        help_text='Line number of the filing form where the contribution is '
                  'itemized (from RCPT_CD.LINE_ITEM)',
    )
    date_received = models.DateField(
        verbose_name='date received',
        null=True,
        help_text='Date the contribution was received (from RCPT_CD.'
                  'RCPT_DATE)'
    )
    date_received_thru = models.DateField(
        verbose_name='date received thru',
        null=True,
        help_text='End date for late contributions received over a range of '
                  'days (from RCPT_CD.DATE_THRU)',
    )
    TRANSACTION_TYPE_CHOICES = (
        ('F', 'Forgiven Loan'),
        ('I', 'Intermediary'),
        ('R', 'Returned (Negative Amount?)'),
        ('T', 'Third Party Repayment'),
        ('X', 'Transfer'),
    )
    transaction_type = models.CharField(
        verbose_name='transaction type',
        max_length=1,
        choices=TRANSACTION_TYPE_CHOICES,
        help_text='Type of transaction (from RCPT_CD.TRAN_TYPE)',
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Form 460 filing (from RCPT_CD.TRAN_ID)'
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text='Reference number for the memo attached to the contribution '
                  '(from RCPT_CD.MEMO_REFNO)',
    )
    CONTRIBUTOR_CD_CHOICES = (
        ('COM', 'Committee'),
        ('IND', 'Individual'),
        ('OFF', 'Officer'),
        ('OTH', 'Other'),
        ('PTY', 'Political Party'),
        ('RCP', 'Recipient committee'),
        ('SCC', 'Small Contributor Committee'),
    )
    contributor_code = models.CharField(
        verbose_name='contributor code',
        max_length=3,
        blank=True,
        choices=CONTRIBUTOR_CD_CHOICES,
        help_text='Code describing the contributor (from RCPT_CD.ENTITY_CD)',
    )
    contributor_committee_id = models.CharField(
        verbose_name='committee id',
        max_length=9,
        blank=True,
        help_text="Contributor's filer identification number, if it is a "
                  "committee (from RCPT_CD.CMTE_ID)",
        )
    contributor_title = models.CharField(
        verbose_name='contributor title',
        max_length=10,
        blank=True,
        help_text='Name title of the contributor (from RCPT_CD.CTRIB_NAMT)',
    )
    contributor_lastname = models.CharField(
        verbose_name='contributor lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the contributor or business name (from '
                  'RCPT_CD.CTRIB_NAML)',
    )
    contributor_firstname = models.CharField(
        verbose_name='contributor firstname',
        max_length=45,
        help_text='First name of the contributor (from RCPT_CD.CTRIB_NAMF)',
    )
    contributor_name_suffix = models.CharField(
        verbose_name='contributor name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the contributor (from RCPT_CD.CTRIB_NAMS)',
    )
    contributor_city = models.CharField(
        verbose_name='contributor city',
        max_length=30,
        blank=True,
        help_text='City of the contributor (from RCPT_CD.CTRIB_CITY)',
    )
    contributor_state = models.CharField(
        verbose_name='contributor state',
        max_length=2,
        blank=True,
        help_text='State of the contributor (from RCPT_CD.CTRIB_ST)',
    )
    contributor_zip = models.CharField(
        verbose_name='contributor zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'contributor (from RCPT_CD.CTRIB_ZIP4)',
    )
    contributor_employer = models.CharField(
        verbose_name='contributor employer',
        max_length=200,
        blank=True,
        help_text='Employer of the contributor (from RCPT_CD.CTRIB_EMP)',
    )
    contributor_occupation = models.CharField(
        verbose_name='contributor occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the contributor (from RCPT_CD.CTRIB_OCC)',
    )
    contributor_is_self_employed = models.BooleanField(
        verbose_name='contributor is self employed',
        default=False,
        help_text='Indicates whether or not the contributor is self-employed'
                  '(from RCPT_CD.CTRIB_SELF)',
    )
    intermediary_committee_id = models.CharField(
        verbose_name='intermediary committee id',
        blank=True,
        max_length=9,
        help_text="Intermediary's filer identification number, if it is a "
                  "committee (from RCPT_CD.INTR_CMTEID)",
    ) 
    intermediary_title = models.CharField(
        verbose_name='intermediary title',
        max_length=10,
        blank=True,
        help_text='Name title of the intermediary (from RCPT_CD.INTR_NAMT)',
    )
    intermediary_lastname = models.CharField(
        verbose_name='intermediary lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the intermediary or business name (from '
                  'RCPT_CD.INTR_NAML)',
    )
    intermediary_firstname = models.CharField(
        verbose_name='intermediary firstname',
        max_length=45,
        help_text='First name of the intermediary (from RCPT_CD.INTR_NAMF)',
    )
    intermediary_name_suffix = models.CharField(
        verbose_name='intermediary name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the intermediary (from RCPT_CD.INTR_NAMS)',
    )
    intermediary_city = models.CharField(
        verbose_name='intermediary city',
        max_length=30,
        blank=True,
        help_text='City of the intermediary (from RCPT_CD.INTR_CITY)',
    )
    intermediary_state = models.CharField(
        verbose_name='intermediary state',
        max_length=2,
        blank=True,
        help_text='State of the intermediary (from RCPT_CD.INTR_ST)',
    )
    intermediary_zip = models.CharField(
        verbose_name='intermediary zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'intermediary (from RCPT_CD.INTR_ZIP4)',
    )
    intermediary_employer = models.CharField(
        verbose_name='intermediary employer',
        max_length=200,
        blank=True,
        help_text='Employer of the intermediary (from RCPT_CD.INTR_EMP)',
    )
    intermediary_occupation = models.CharField(
        verbose_name='intermediary occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the intermediary (from RCPT_CD.INTR_OCC)',
    )
    intermediary_is_self_employed = models.BooleanField(
        verbose_name='intermediary is self employed',
        default=False,
        help_text='(from S497_CD.INTR_SELF)',
    )
    cumulative_ytd_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="Cumulative year-to-date amount given by the contributor "
                  "as of the given Form 460 filing (from RCPT_CD.CUM_YTD)",
    )
    cumulative_election_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="For filers subject to contribution limits, cumulative "
                  "amount given by the contributor during the election "
                  "cycle as of the given Form 460 filing (from RCPT_CD."
                  "CUM_OTH)"
    )

    class Meta:
        abstract = True


class MonetaryContributionBase(ContributionBase):
    """
    Abstract base model for monetary contributions, as itemized in Schedule A 
    of the Form 460 filings.
    """
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount received in the period covered by the filing (from "
                  "RCPT_CD.AMOUNT)"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class MonetaryContribution(MonetaryContributionBase):
    """
    Monetary contributions, as itemized on Schedule A of Form 460 filings.

    Includes transactions itemized on the most recent amendment to the given
    Form 460 filing. For transactions itemized on any version of a Form 460
    filing, see monetarycontributionversion.

    Derived from RCPT_CD records where FORM_TYPE is 'A'.
    """
    filing = models.ForeignKey(
        'Form460',
        related_name='itemized_monetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class MonetaryContributionVersion(MonetaryContributionBase):
    """
    Every version of a monetary contribution, as itemized on Schedule A of
    each version of each Form 460 filing.

    For contributions itemized on the most recent version of the Form 460 
    filing, see monetarycontribution.

    Derived from RCPT_CD records where FORM_TYPE is 'A'.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        null=False,
        help_text='Unique identification number for the Form 460 filing ('
                  'from RCPT_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 460 filing, with 0 '
                  'representing the initial filing (from RCPT_CD.AMEND_ID)',
    )
    filing_version = models.ForeignKey(
        'Form460Version',
        related_name='itemized_monetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)
        index_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (self.filing_id, self.amend_id, self.line_item)


class NonMonetaryContributionBase(ContributionBase):
    """
    Abstract base model for non-monetary contributions, as itemized in Schedule
    C of the Form 460 filings.
    """
    fair_market_value = models.DecimalField(
        verbose_name='fair market value',
        decimal_places=2,
        max_digits=14,
        help_text="Amount it would cost to purchase the donated goods or "
                  "services on the open market (from RCPT_CD.AMOUNT)"
    )
    contribution_description = models.CharField(
        max_length=90,
        blank=True,
        help_text="Description of the contributed goods or services (from "
                  "RCPT_CD.CTRIB_DSCR)"
    )
    
    class Meta:
        abstract = True
        verbose_name = 'Nonmonetary contribution'
        verbose_name_plural = 'Nonmonetary contributions'


@python_2_unicode_compatible
class NonMonetaryContribution(NonMonetaryContributionBase):
    """
    Non-monetary contributions, as itemized on Schedule C of Form 460 filings.

    Includes transactions itemized on the most recent amendment to the given
    Form 460 filing. For transactions itemized on any version of a Form 460
    filing, see nonmonetarycontributionversion.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing = models.ForeignKey(
        'Form460',
        related_name='itemized_nonmonetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = 'Nonmonetary contribution version'
        verbose_name_plural = 'Nonmonetary contributions versions'

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class NonMonetaryContributionVersion(NonMonetaryContributionBase):
    """
    Every version of a non-monetary contribution, as itemized on Schedule A of
    each version of each Form 460 filing.

    For contributions itemized on the most recent version of the Form 460 
    filing, see monetarycontribution.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        null=False,
        help_text='Unique identification number for the Form 460 filing ('
                  'from RCPT_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 460 filing, with 0 '
                  'representing the initial filing (from RCPT_CD.AMEND_ID)',
    )
    filing_version = models.ForeignKey(
        'Form460Version',
        related_name='itemized_nonmonetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)
        index_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (self.filing_id, self.amend_id, self.line_item)


class LateContributionBase(models.Model):
    """
    Abstract base model for late contributions received or made, as itemized on
    Schedule 497.

    Records are derived from the S497_CD table.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        db_index=True,
        null=False,
        help_text='Line number of the filing form where the transaction is '
                  'itemized (from S497_CD.LINE_ITEM)',
    )
    date_received = models.DateField(
        verbose_name='date received',
        db_index=True,
        null=True,
        help_text='Date the late contribution was received (from S497_CD.'
                  'CTRIB_DATE, unless NULL then from S497_CD.DATE_THRU)'
    )
    date_received_thru = models.DateField(
        verbose_name='date received thru',
        null=True,
        help_text='End date for late contributions received over a range of '
                  'days(from S497_CD.DATE_THRU)',
    )
    amount_received = models.DecimalField(
        verbose_name='amount received',
        decimal_places=2,
        max_digits=16,
        help_text='Dollar amount received (from S497_CD.AMOUNT)',
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        db_index=True,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Schedule 497 filing (from S497_CD.TRAN_ID)'
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text='Reference number for the memo attached to the transaction '
                  '(from S497_CD.MEMO_REFNO)',
    )

    class Meta:
        abstract = True


class LateContributionReceivedBase(LateContributionBase):
    """
    Abstract base model for late contributions received, as itemized in Part 1
    of Schedule 497.
    """
    CONTRIBUTOR_CD_CHOICES = (
        ('BNM', 'Ballot measure name/title'),
        ('CAO', 'Candidate/officeholder'),
        ('COM', 'Committee'),
        ('CTL', 'Controlled committee'),
        ('IND', 'Individual'),
        ('OFF', 'Officer'),
        ('OTH', 'Other'),
        ('PTY', 'Political Party'),
        ('RCP', 'Recipient committee'),
        ('SCC', 'Small Contributor Committee'),
    )
    contributor_code = models.CharField(
        verbose_name='contributor code',
        max_length=3,
        blank=True,
        choices=CONTRIBUTOR_CD_CHOICES,
        help_text='Code describing the contributor (from S497_CD.ENTITY_CD)',
    )
    contributor_committee_id = models.CharField(
        verbose_name='committee id',
        max_length=9,
        blank=True,
        help_text="Contributor's filer identification number, if it is a "
                  "committee (from RCPT_CD.CMTE_ID)",
        )
    contributor_title = models.CharField(
        verbose_name='contributor title',
        max_length=10,
        blank=True,
        help_text='Name title of the contributor (from S497_CD.ENTY_NAMT)',
    )
    contributor_lastname = models.CharField(
        verbose_name='contributor lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the contributor (from S497_CD.ENTY_NAML)',
    )
    contributor_firstname = models.CharField(
        verbose_name='contributor firstname',
        max_length=45,
        help_text='First name of the contributor (from S497_CD.ENTY_NAMF)',
    )
    contributor_name_suffix = models.CharField(
        verbose_name='contributor name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the contributor (from S497_CD.ENTY_NAMS)',
    )
    contributor_city = models.CharField(
        verbose_name='contributor city',
        max_length=30,
        blank=True,
        help_text='City of the contributor (from S497_CD.ENTY_CITY)',
    )
    contributor_state = models.CharField(
        verbose_name='contributor state',
        max_length=2,
        blank=True,
        help_text='State of the contributor (from S497_CD.ENTY_ST)',
    )
    contributor_zip = models.CharField(
        verbose_name='contributor zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'contributor (from S497_CD.ENTY_ZIP4)',
    )
    contributor_employer = models.CharField(
        verbose_name='contributor employer',
        max_length=200,
        blank=True,
        help_text='Employer of the contributor (from S497_CD.CTRIB_EMP)',
    )
    contributor_occupation = models.CharField(
        verbose_name='contributor occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the contributor (from S497_CD.CTRIB_OCC)',
    )
    contributor_is_self_employed = models.BooleanField(
        verbose_name='contributor is self employed',
        default=False,
        help_text='Indicates whether or not the contributor is self-employed'
                  '(from S497_CD.CTRIB_SELF)',
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class LateContributionReceived(LateContributionReceivedBase):
    """
    Late contributions received, as itemized on Part 1 of Schedule 497 filings.

    Includes transactions itemized on the most recent amendment to the given
    Schedule 497 filing. For transactions itemized on any version of a 
    Schedule 497 filing, see latecontributionreceivedversion.

    Derived from S497_CD records where FORM_TYPE is 'F497P1'.
    """
    filing = models.ForeignKey(
        'Schedule497',
        related_name='contributions_received',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name_plural = 'Late contributions received'

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class LateContributionReceivedVersion(LateContributionReceivedBase):
    """
    Every version of a late contribution received transaction, as itemized on 
    Part 1 of each version of each Schedule 497 filings.

    For contributions itemized on the most recent version of the Schedule 497 
    filing, see latecontributionreceived.

    Derived from S497_CD records where FORM_TYPE is 'F497P1'.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        null=False,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Schedule 497 filing, with 0 '
                  'representing the initial filing (from S497_CD.AMEND_ID)',
    )
    filing_version = models.ForeignKey(
        'Schedule497Version',
        related_name='contributions_received',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Schedule 497 '
                  'that includes the received contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)
        index_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (self.filing_id, self.amend_id, self.line_item)


class LateContributionMadeBase(LateContributionBase):
    """
    Abstract base model for late contributions made, as itemized in Part 2
    of Schedule 497.
    """
    RECIPIENT_CD_CHOICES = (
        ('BNM', 'Ballot measure name/title'),
        ('CAO', 'Candidate/officeholder'),
        ('COM', 'Committee'),
        ('CTL', 'Controlled committee'),
        ('IND', 'Individual'),
        ('OTH', 'Other'),
        ('PTY', 'Political Party'),
        ('RCP', 'Recipient committee'),
        ('SCC', 'Small Contributor Committee'),
    )
    recipient_code = models.CharField(
        verbose_name='recipient code',
        max_length=3,
        blank=True,
        choices=RECIPIENT_CD_CHOICES,
        help_text='Code describing the recipient (from S497_CD.ENTITY_CD)',
    )
    recipient_committee_id = models.CharField(
            verbose_name='recipient committee id',
            max_length=9,
            blank=True,
            help_text='Filer identification number identifying the recipient if it'
                      'is a committee (from S497_CD.CMTE_ID)',
        )
    recipient_title = models.CharField(
        verbose_name='recipient title',
        max_length=10,
        blank=True,
        help_text='Name title of the recipient (from S497_CD.ENTY_NAMT)',
    )
    recipient_lastname = models.CharField(
        verbose_name='recipient lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the recipient (from S497_CD.ENTY_NAML)',
    )
    recipient_firstname = models.CharField(
        verbose_name='recipient firstname',
        max_length=45,
        help_text='First name of the recipient (from S497_CD.ENTY_NAMF)',
    )
    recipient_name_suffix = models.CharField(
        verbose_name='recipient name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the recipient (from S497_CD.ENTY_NAMS)',
    )
    recipient_city = models.CharField(
        verbose_name='recipient city',
        max_length=30,
        blank=True,
        help_text='City of the recipient (from S497_CD.ENTY_CITY)',
    )
    recipient_state = models.CharField(
        verbose_name='recipient state',
        max_length=2,
        blank=True,
        help_text='State of the recipient (from S497_CD.ENTY_ST)',
    )
    recipient_zip = models.CharField(
        verbose_name='recipient zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'recipient (from S497_CD.ENTY_ZIP4)',
    )
    candidate_id = models.CharField(
        verbose_name='candidate id',
        max_length=9,
        blank=True,
        help_text = 'Identifies the candidate to whom the contribution is '
                    'connected (from S497_CD.CAND_ID). This can be translated '
                    'to the filer_id by joining to FILER_XREF_CD.',
    )
    candidate_title = models.CharField(
        verbose_name='candidate title',
        max_length=10,
        blank=True,
        help_text = 'Name title of the candidate to whom the contribution is '
                    'connected (from S497_CD.CAND_NAMT)',
    )
    candidate_lastname = models.CharField(
        verbose_name='candidate last name',
        max_length=200,
        blank=True,
        help_text = 'Last name of the candidate to whom the contribution is '
                    'connected (S497_CD.CAND_NAML)',
    )
    candidate_firstname = models.CharField(
        verbose_name='candidate first name',
        max_length=45,
        blank=True,
        help_text = 'First name of the candidate to whom the contribution is '
                    'connected (S497_CD.CAND_NAMF)',
    )
    candidate_namesuffix = models.CharField(
        verbose_name='candidate name suffix',
        max_length=10,
        blank=True,
        help_text = 'Name suffix of the candidate to whom the contribution is '
                    'connected (S497_CD.CAND_NAMS)',
    )
    candidate_office_code = models.CharField(
        verbose_name='candidate office code',
        max_length=3,
        blank=True,
        help_text='Code describing the office sought sought by the candidate '
                  '(from S497_CD.OFFICE_CD)',
    )
    candidate_office_description = models.CharField(
        verbose_name='candidate office description',
        max_length=40,
        blank=True,
        help_text='Full description of the office sought by the candidate '
                  '(from S497_CD.OFFIC_DSCR)',
    )
    candidate_jurisdiction_code = models.CharField(
        verbose_name='candidate jursidiction code',
        max_length=3,
        blank=True,
        help_text='Code describing the jurisdiction of office sought by the '
                  'candidate (from S497_CD.JURIS_CD)',
    )
    candidate_jurisdiction_description = models.CharField(
        verbose_name='candidate jurisdiction description',
        max_length=40,
        blank=True,
        help_text='Full description of the jurisdiction of the office sought '
                  'by the candidate (from S497_CD.JURIS_DSCR)',
    )
    candidate_district = models.CharField(
        verbose_name='candidate district',
        max_length=3,
        blank=True,
        help_text='District of the office sought by the candidate (from '
                  'S497_CD.DIST_NO)',
    )
    ballot_measure_name = models.CharField(
        verbose_name='Ballot measure name',
        max_length=200,
        blank=True,
        help_text='Name of the ballot measure supported or opposed by the '
                  'recipient (from S497_CD.BAL_NAME)',
    )
    ballot_measure_number = models.CharField(
        verbose_name='Ballot measure number',
        max_length=7,
        blank=True,
        help_text='Ballot measure number (from S497_CD.BAL_NUM)',
    )
    ballot_measure_jurisdiction = models.CharField(
        verbose_name='ballot measure jurisdiction',
        max_length=40,
        blank=True,
        help_text='Jurisdiction of the ballot measure supported or opposed by '
                  'the recipient (from S497_CD.BAL_JURIS)',
    )
    SUPPORT_OPPOSITION_CODE_CHOICES = (
        ('O', 'Opposition'),
        ('S', 'Support'),
    )
    support_opposition_code = models.CharField(
        verbose_name='support opposition code',
        max_length=1,
        choices=SUPPORT_OPPOSITION_CODE_CHOICES,
        blank=True,
        help_text='Code describing whether the contribuitor supports or opposes'
                  'the candidate or ballot measure (from S497_CD.SUP_OPP_CD)',
    )
    election_date = models.DateField(
        verbose_name='election date',
        null=True,
        help_text='Date of the election (from S497_CD.ELEC_DATE)',
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class LateContributionMade(LateContributionMadeBase):
    """
    Late contributions made, as itemized on Part 2 of Schedule 497 filings.

    Includes transactions itemized on the most recent amendment to the given
    Schedule 497 filing. For transactions itemized on any version of a 
    Schedule 497 filing, see latecontributionmadeversion.

    Derived from S497_CD records where FORM_TYPE is 'F497P2'.
    """
    filing = models.ForeignKey(
        'Schedule497',
        related_name='contributions_made',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name_plural = 'Late contributions made'

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class LateContributionMadeVersion(LateContributionMadeBase):
    """
    Every version of a late contribution made transaction, as itemized on 
    Part 2 of each version of each Schedule 497 filings.

    For contributions itemized on the most recent version of the Schedule 497 
    filing, see latecontributionmade.

    Derived from S497_CD records where FORM_TYPE is 'F497P2'.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        null=False,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Schedule 497 filing, with 0 '
                  'representing the initial filing (from S497_CD.AMEND_ID)',
    )
    filing_version = models.ForeignKey(
        'Schedule497Version',
        related_name='contributions_made',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Schedule 497 '
                  'that includes the given contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)
        index_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)


    def __str__(self):
        return '%s-%s-%s' % (self.filing_id, self.amend_id, self.line_item)