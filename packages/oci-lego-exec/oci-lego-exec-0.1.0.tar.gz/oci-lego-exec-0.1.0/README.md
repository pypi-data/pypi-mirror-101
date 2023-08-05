# Oracle Cloud infrastructure DNS Authenticator script for LEGO

https://go-acme.github.io/lego/dns/exec/
 
Script automates the process of `dns-01` challenge by managing TXT records using the Oracle Cloud Infrastructure
DNS service.

## Why?

This package provides simple `ocilego` utility to being executed by lego in `acme_certificate`
terraform resource. Native `oraclecloud` provider is difficult to use because of uncommon authentication
variables: https://github.com/go-acme/lego/issues/1380

## Installation

```shell
pip3 install oci-lego-exec
```

## Usage

```terraform
resource "acme_certificate" "certificate" {
  ...

  dns_challenge {
    provider = "exec"

    config = {
      "EXEC_PATH" = "ocilego"
    }
  }
}
```

## Requirements
```
oci
```