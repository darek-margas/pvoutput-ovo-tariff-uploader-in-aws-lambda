# This is AWS Lambda-packed OVO to PVO uploader
To run ich cheap in te cloud, AWS Lambda seems best fit (to me at least).

So, here it is. 
I was inspired by Adam Petrovic and his script idea.
(https://github.com/adampetrovic/pvoutput-tariff)

To have it running in Lambda, two files and layers pack have to be installed.

Don't forget the below to work requires donation for PVO and extended atributes setup. Do it first, certainly before testing. Use "last" in parameters.

Quick install:
- Create custom empty Lambda in AWS Lambda console
- Go to "code" and upload lambda_function.py and config.yaml to the code directory
- Modify config.yaml to match your tariff and extended attribute. For now only import works so ignore export setting
- Go to Layers in Lambda console and upload layers pvo-layers.zip file while creating new custom layer
- Now go back to function/code and down the bottom add custom layer from what you just made
- Make sure you "re-deploy" it now
- Create custom json test from sample file by adding your key and id
- Test if it works. Quickest probably from US east coast.
- If it works, create cron scheduler for your new function using json event you just tested with. Should be every 5 minutes.
