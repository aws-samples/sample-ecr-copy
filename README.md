# Copy ECR Container Images Into Cross-Account and Cross-Region AWS Accounts

## Description
This pattern describes how to copy all tagged images from an existing Amazon ECR repository into another AWS accounts and regions using a serverless orchestration approach. The pattern uses AWS Step Functions to orchestrate the copying workflow and AWS Lambda functions to efficiently copy large container images. The solution addresses common MLOps challenges where AI teams need to distribute containerized machine learning models, frameworks (PyTorch, TensorFlow, Hugging Face), and dependencies into a new account and a new region to overcome service limits and access optimal GPU compute resources. 

This solution enables selective copying of ECR repositories across AWS accounts and regions. For example, you can use this solution to copy specific ECR repositories from a source account and region to a destination account and a different region.


**The code in this repository helps you set up the following target architecture.**


![Target architecture diagram](architecture/ECR%20Copy%20Cross%20Account.jpg) 

## For prerequisites and instructions for using this AWS Prescriptive Guidance pattern, see [Copy ECR Container Images Into Cross-Account and Cross-Region AWS Accounts](https://apg-library.amazonaws.com/content-viewer/787185e7-664b-4ed8-b30f-1d9507f13377).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.