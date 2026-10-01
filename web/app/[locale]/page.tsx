import { useTranslations } from "next-intl";
import { setRequestLocale } from "next-intl/server";
import { use } from "react";
import { Link } from "@/i18n/navigation";
import { routing } from "@/i18n/routing";

type Props = { params: Promise<{ locale: string }> };

export default function HomePage({ params }: Props) {
  const { locale } = use(params);
  setRequestLocale(locale);
  const t = useTranslations("home");
  const tl = useTranslations("locales");

  return (
    <main className="mx-auto max-w-4xl px-4 py-12">
      <nav aria-label={t("languageNav")} className="mb-8 flex gap-4 text-sm">
        {routing.locales.map((l) => (
          <Link key={l} href="/" locale={l} aria-current={l === locale ? "page" : undefined}>
            {tl(l)}
          </Link>
        ))}
      </nav>
      <h1 className="text-3xl font-semibold">{t("title")}</h1>
      <p className="mt-4 text-lg">{t("tagline")}</p>
      <p className="mt-8 text-[var(--muted)]">{t("placeholder")}</p>
    </main>
  );
}
