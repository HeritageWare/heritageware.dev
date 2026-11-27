# heritageware.dev

The Foundation website is a static site built with Python 3.10 or newer and its standard library. It uses relative links so the same build works at the Pages project URL and the custom domain. There is no backend, analytics, or third-party runtime asset.

```sh
python3 build.py
python3 check.py
```

The generated artifact is in `_site/`. The build job publishes a downloadable artifact for pull request previews. The link check covers generated navigation, fragments and assets at both deployment paths. Public GitHub links depend on publication of the relevant repositories.

See [deployment instructions](DEPLOYMENT.md) for Page setup, verification, and DNS. Update the compatibility data from a published compatibility-suite CI run when available. The initial empty dataset states that no results have been published.

## License

Original source code, build configuration, and executable examples are licensed under [Apache-2.0](LICENSE). Original prose documentation is licensed under [CC BY 4.0](LICENSE-DOCS). Generated website pages retain the applicable terms of their code and prose sources. Third-party material retains its own terms.
