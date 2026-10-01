import { routing } from "@/i18n/routing";

const target = `/${routing.defaultLocale}/`;

// Static export has no middleware: redirect "/" to the default locale with a meta refresh,
// which works without JavaScript and for crawlers.
export default function RootPage() {
  return (
    <html lang={routing.defaultLocale}>
      <head>
        <meta httpEquiv="refresh" content={`0; url=${target}`} />
        <link rel="canonical" href={target} />
      </head>
      <body>
        <a href={target}>{target}</a>
      </body>
    </html>
  );
}
