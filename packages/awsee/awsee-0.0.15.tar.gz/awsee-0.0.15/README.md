**AWSee**
---
---
Command line tool that helps handle multiple AWS Account Credentials (its Roles and MFAs), when working with AWSCLI sessions. 

It opens and controls AWS Sessions using a command-line tool, allowing performing one or all of the following tasks:
- Start session using a MFA Token
- Assume a Role
- Open a session in the same or another terminal window
- Keep track of session information (expiration)
- "Injects" alias/DOSKEY commands in your opened session, that's configurable. Entries in file, examples:
  - alias s3='aws s3 ls'
  - alias info='awsee -i'

Plus, it also tries (if allowed by your AWS Polices) automatically bring and save locally information about your MFA-Devices to be used later on. 

When not possible to retrieve account information automactically (due to security reasons), you still can register it locally using this tool. You can save and keep them updated, to help to deal with your AWS Sessions, like:
- MFA-Devices
- Roles

---

For more information and details, check here:

[AWSee](https://ualter.github.io/awsee-site/)