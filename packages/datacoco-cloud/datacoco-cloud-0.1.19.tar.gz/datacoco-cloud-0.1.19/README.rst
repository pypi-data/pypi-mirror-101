datacoco-cloud
=================

.. image:: https://badge.fury.io/py/datacoco-cloud.svg
    :target: https://badge.fury.io/py/datacoco-cloud
    :alt: PyPI Version

.. image:: https://readthedocs.org/projects/datacococloud/badge/?version=latest
    :target: https://datacococloud.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/8b768d9639a94456b8574158122f36ae
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-cloud?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-cloud&amp;utm_campaign=Badge_Grade
    :alt: Code Quality Grade

.. image:: https://api.codacy.com/project/badge/Coverage/36df276fb1fe47d18ff1ea8c7a0aa522
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-cloud?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-cloud&amp;utm_campaign=Badge_Coverage
    :alt: Coverage

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
    :target: https://github.com/equinoxfitness/datacoco-cloud/blob/master/CODE_OF_CONDUCT.rst
    :alt: Code of Conduct

Datacoco-cloud contains interaction classes S3, Athena, SES, SNS, SQS, ECS, EMR, Cloudwatch logs

Installation
------------

datacoco-cloud requires Python 3.6+

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install datacoco-cloud

Usage
~~~~~

S3toS3Interaction
^^^^^^^^^^^^^^^^^

Please take note that all AWS Permissions in `IAM` and `Bucket Policies` need to be properly in place for this utility to work.
`Click here for more details <https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-s3/>`_.

Sample Code
"""""""""""

::

    # Import the class first
    from datacococloud.s3_to_s3_interaction import S3toS3Interaction
    
    # Instantiate with your key pairs
    s3toS3 = S3toS3Interaction(<source_aws_key>,
                               <source_aws_secret>,
                               <target_aws_key>,
                               <target_aws_secret>,
                               <source_aws_region>(optional default='us-east-1'),
                               <target_aws_region>(optional default='us-east-1')
                               )

    # Copying the files
    s3toS3.duplicate_objects(<source_bucket>,
                             <target_bucket>,
                             <source_bucket_prefix>,
                             <target_path>,
                             <source_bucket_suffix>(optional default=''))


    # Moving the files
    # This deletes the file from the source after copying to the target
    s3toS3.move_objects(<source_bucket>,
                             <target_bucket>,
                             <source_bucket_prefix>,
                             <target_path>,
                             <source_bucket_suffix>(optional default=''))

Terms
"""""
* ``source_aws_key`` - AWS key ID from source account
* ``source_aws_secret`` - AWS key secret from source account
* ``target_aws_key`` - AWS key ID from target account
* ``target_aws_secret`` - AWS key secret from target account
* ``source_aws_region`` - AWS region of the source `S3` bucket 
* ``target_aws_region`` - AWS region of the source `S3` bucket

* ``source_bucket`` - S3 bucket of the source file
* ``target_bucket`` - S3 bucket where the files are going to be transferred
* ``source_bucket_prefix`` - The prefix of the files to transfer from the source
    `Note:` Add ``/`` at the end to specify a folder e.g (`files/`)
* ``target_path`` - the Path at the target bucket where the files will be transferred
    `Note:` if the the folder does not exist, it will auto create it for you
* ``source_bucket_prefix`` - The suffix of the files to transfer from the source






Quickstart
----------

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install --upgrade pip
    pip install -r requirements_dev.txt


Development
-----------

Getting Started
~~~~~~~~~~~~~~~

It is recommended to use the steps below to set up a virtual environment for development:

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install -r requirements.txt

Testing
~~~~~~~

::

    pip install -r requirements_dev.txt

To run the testing suite, simply run the command: ``tox`` or ``python -m unittest discover tests``



Contributing
------------

Contributions to datacoco\_cloud are welcome!

Please reference guidelines to help with setting up your development
environment
`here <https://github.com/equinoxfitness/datacoco-cloud/blob/master/CONTRIBUTING.rst>`__.