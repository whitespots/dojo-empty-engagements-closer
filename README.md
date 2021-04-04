# dojo-empty-engagements-closer

Just a small tool to close DefectDojo empty engagements

```bash
$ docker build -t dojo_closer .


$ docker run --rm --name dojo_closer \
  -e DOJO_TOKEN=token_for_defectdojo_api \
  -e DOJO_BASE_URL=https://defectdojo.site.com 
```

