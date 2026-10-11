// Helpers for the Epidaurian iamata catalogue (src/data/iamata.json): the
// Epigraphy index, the tale pages, /geographies and the journal entries.
import sites from '../data/sites.json';

// PHI's text of the stele. PHI's terms allow reading, not copying, so the
// site links to it instead of reproducing the Greek.
export const phiUrl = (tale) => `https://epigraphy.packhum.org/text/${tale.phi}`;

export const taleUrl = (tale) => `/epigraphy/iamata/${tale.n}`;

export const originOf = (tale) => (tale.origin ? sites.find((s) => s.id === tale.origin) : null);

// "Ithmonika (2)": the short label used in lists.
export const taleLabel = (tale) => `${tale.n}. ${tale.petitioner}`;
