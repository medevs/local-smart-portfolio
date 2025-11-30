/**
 * Certifications for Ahmed Oublihi
 */

export interface Certification {
  name: string;
  issuer: string;
  date: string;
  description?: string;
  credentialId?: string;
  link?: string;
}

export const certifications: Certification[] = [
  {
    name: "Microsoft Certified Professional",
    issuer: "Microsoft",
    date: "May 2018",
    description: "Web Development: HTML5, CSS3, JavaScript",
  },
];

