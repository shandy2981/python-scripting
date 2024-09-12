import click
import boto3

@click.group()
def cli():
    """RDS Backup tool"""
    pass

@cli.command()
@click.option('--rds-instance-id', required=True, help='The ID of the RDS instance to backup.')
@click.option('--s3-bucket', required=True, help='The S3 bucket where the snapshot will be stored.')
def backup(rds_instance_id, s3_bucket):
    """Backup RDS instance to S3"""
    snapshot_id = take_rds_snapshot(rds_instance_id)
    click.echo('f"Snapshot {snapshot_id} taken successfully')
    copy_snapshot_to_s3(snapshot_id, s3_bucket)
    click.echo(f"Snapshot {snapshot_id} copied to S3 bucket {s3_bucket}.")

def take_rds_snapshot(rds_instance_id):
    rds_client = boto3.client('rds')
    snapshot_id = f"{rds_instance_id}-snapshot-{int(time.time())}"
    response = rds_client.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_id,
        DBInstanceIdentifier=rds_instance_id
    )
    return response['DBSnapshot']['DBSnapshotIdentifier']

def copy_snapshot_to_s3(snapshot_id, s3_bucket):
    s3_client = boto3.client('s3')
    s3_client.upload_file(snapshot_id, s3_bucket, f"{snapshot_id}.rds")
