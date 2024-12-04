import boto3

# AWS Boto3 Clients
ec2 = boto3.client('ec2')

def get_unused_volumes():
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
    return volumes

def create_snapshot(volume_id):
    response = ec2.create_snapshot(VolumeId=volume_id, Description=f"Backup for volume {volume_id}")
    print(f"Snapshot created for volume {volume_id}: {response['SnapshotId']}")
    return response['SnapshotId']

def delete_volume(volume_id):
    ec2.delete_volume(VolumeId=volume_id)
    print(f"Deleted volume {volume_id}")

if __name__ == "__main__":
    unused_volumes = get_unused_volumes()
    for volume in unused_volumes:
        volume_id = volume['VolumeId']
        print(f"Processing volume: {volume_id}")
        snapshot_id = create_snapshot(volume_id)
        delete_volume(volume_id)
