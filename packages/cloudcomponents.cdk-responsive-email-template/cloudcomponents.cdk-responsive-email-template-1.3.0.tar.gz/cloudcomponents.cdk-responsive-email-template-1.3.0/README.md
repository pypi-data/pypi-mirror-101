[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-responsive-email-template

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-responsive-email-template)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-responsive-email-template/)

> Responsive [mjml](https://documentation.mjml.io/) email template for aws ses

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-responsive-email-template
```

Python:

```bash
pip install cloudcomponents.cdk-responsive-email-template
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from cloudcomponents.cdk_responsive_email_template import ResponsiveEmailTemplate, TemplatePart

class ResponsiveEmailTemplateStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        ResponsiveEmailTemplate(self, "EmailTemplate",
            template_name="demo",
            subject_part="cloudcomponents - {{ title }}",
            text_part=TemplatePart.from_inline("text message"),
            html_part=TemplatePart.from_inline("""<mjml>
                    <mj-head>
                      <mj-title>cloudcomponents - {{ title }}</mj-title>
                    </mj-head>
                    <mj-body>
                      <mj-section>
                        <mj-column>
                          <mj-text>
                            Hello {{ name }}!
                          </mj-text>
                        </mj-column>
                      </mj-section>
                    </mj-body>
                  </mjml>"""),
            parsing_options=ParsingOptions(
                beautify=True
            )
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-responsive-email-template/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-responsive-email-template/LICENSE)
