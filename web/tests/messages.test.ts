import { describe, expect, it } from "vitest";
import en from "../messages/en.json";
import hy from "../messages/hy.json";
import ru from "../messages/ru.json";

function keys(obj: object, prefix = ""): string[] {
  return Object.entries(obj).flatMap(([k, v]) =>
    v !== null && typeof v === "object" ? keys(v as object, `${prefix}${k}.`) : [`${prefix}${k}`],
  );
}

function values(obj: object): unknown[] {
  return Object.values(obj).flatMap((v) => (v !== null && typeof v === "object" ? values(v) : [v]));
}

// Spec 14.2: no untranslated keys in any locale.
describe("messages", () => {
  const reference = keys(hy).sort();

  it.each([
    ["ru", ru],
    ["en", en],
  ])("%s has the same keys as hy", (_, messages) => {
    expect(keys(messages).sort()).toEqual(reference);
  });

  it.each([
    ["hy", hy],
    ["ru", ru],
    ["en", en],
  ])("%s has no empty strings", (_, messages) => {
    for (const v of values(messages))
      expect(typeof v === "string" && v.trim().length > 0).toBe(true);
  });
});
