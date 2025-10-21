# Copy ECR Container Images Into Cross-Account and Cross-Region AWS Accounts

## Description
This pattern shows you how to use a serverless approach to replicate tagged images from existing Amazon Elastic Container Registry (Amazon ECR) repositories to other AWS accounts and Regions. The solution uses AWS Step Functions to manage the replication workflow and AWS Lambda functions to copy large container images.

Amazon ECR uses native [cross-Region](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-settings-examples.html#registry-settings-examples-crr-single) and [cross-account](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-settings-examples.html#registry-settings-examples-crossaccount) replication features that replicate container images across Regions and accounts. But these features only replicate images from the moment replication is turned on. There is no mechanism to replicate existing images in different Regions and accounts. 

This pattern helps artificial intelligence (AI) teams distribute containerized machine learning (ML) models, frameworks (for example, PyTorch, TensorFlow, and Hugging Face), and dependencies to other accounts and Regions. This can help you overcome service limits and optimize GPU compute resources. You can also selectively replicate Amazon ECR repositories from specific source accounts and Regions. For more information, see [Cross-Region replication in Amazon ECR has landed.](https://aws.amazon.com/blogs/containers/cross-region-replication-in-amazon-ecr-has-landed/)


**The code in this repository helps you set up the following target architecture.**


![Target architecture diagram](architecture/ECR%20Copy%20Cross%20Account.jpg) 

## For prerequisites and instructions for using this AWS Prescriptive Guidance pattern, see [Copy ECR Container Images Into Cross-Account and Cross-Region AWS Accounts](https://apg-library.amazonaws.com/content-viewer/787185e7-664b-4ed8-b30f-1d9507f13377).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.