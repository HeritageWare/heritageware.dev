# GitHub Pages deployment

## Staging

1. Publish the website and its linked Foundation repositories after owner approval.
2. Open repository **Settings → Pages → Build and deployment** and select **GitHub Actions** as the source.
3. Run **Actions → Website → Run workflow** on `main`. If the initial push fired before Pages was enabled, use this manual run to deploy the same commit.
4. Confirm the workflow's build, link-check and deployment steps. Open `https://heritageware.github.io/heritageware.dev/` and navigate through the site. Confirm the public GitHub destinations resolve.

[GitHub Actions publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Verified custom domain

1. Confirm the owner approves DNS changes. In the organization's **Settings → Pages**, choose **Add a domain** and enter `heritageware.dev`. Add the TXT record exactly as GitHub displays it, verify in GitHub, and keep the TXT record after verification.
2. Inventory the actual Cloudflare records and confirm which web records serve other uses. In the website repository's **Settings → Pages**, set the custom domain to `heritageware.dev`. The Actions publishing source manages the domain through settings.
3. When authorized, point the apex to GitHub Pages using these four DNS-only A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, and `185.199.111.153`. If using IPv6 records, use `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, and `2606:50c0:8003::153`. Set `www` to a DNS-only CNAME for `heritageware.github.io`. Replace obsolete conflicting web records with the owner's approval. Preserve MX, SPF, and existing TXT records. Avoid wildcard records.
4. Recheck apex and www DNS, then enable **Enforce HTTPS** when GitHub issues the certificate. Check that both HTTPS names serve the site or redirect as intended. Verify public links after the domain transition.

GitHub handles custom domains through Pages settings for Actions deployments. A checked-in CNAME file applies to branch publishing. If switching to branch publishing later, configure the approved apex domain and place a single `heritageware.dev` line in the publishing source's CNAME file as GitHub documents.

[Verify a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages) · [Manage a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
