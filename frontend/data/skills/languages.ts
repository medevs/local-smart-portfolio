/**
 * Language proficiencies
 */

export interface Language {
  name: string;
  level: string;
}

export const languages: Language[] = [
  { name: "German", level: "Very Good (Sehr gute Kenntnisse)" },
  { name: "English", level: "Good (Gute Kenntnisse)" },
  { name: "French", level: "Basic (Grundkenntnisse)" },
  { name: "Tamazight (Berberisch)", level: "Native (Muttersprache)" },
  { name: "Arabic", level: "Native (Muttersprache)" },
];

