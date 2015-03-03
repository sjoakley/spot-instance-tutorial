#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "The name of the EC2 keypair is required."

OUTPUT_PATH=/tmp/spot_request.json

# Launch an instance to act as the web server.
LAUNCH_SPECIFICATION="
{
    \"ImageId\": \"ami-12296b7a\",
    \"InstanceType\": \"m2.4xlarge\",
    \"SubnetId\": \"subnet-ac59ebf5\",
    \"SecurityGroupIds\": [\"sg-ff1fab9b\"],
    \"KeyName\": \"$1\"
}
"
aws ec2 request-spot-instances \
    --spot-price '0.2' \
    --instance-count 1 \
    --type "one-time" \
    --launch-specification "$LAUNCH_SPECIFICATION" \
    > $OUTPUT_PATH

echo "Requested spot instance..."
# cat $OUTPUT_PATH

spot_request_id=`objectpath -e '$.SpotInstanceRequests[0].SpotInstanceRequestId' $OUTPUT_PATH | sed 's/"//g'`

# Tag the spot instance request.
echo "Tagging request $spot_request_id"
aws ec2 create-tags --resources $spot_request_id --tags Key=Name,Value=spot-$USER

# Launch the instances to act as the load generators.
# TODO: Complete this.
