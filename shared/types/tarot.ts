export interface Detail {
  type: 'visual' | 'symbolism' | 'interpretation'
  content: string
}

export interface Element {
  label: string
  x: number
  y: number
  r: number
  details: Detail[]
}

export interface Scenario {
  type: 'relationship' | 'business' | 'wealth'
  content: string
}

export interface Meaning {
  meaning: string
  keywords: string[]
  summary: string
  scenarios: Scenario[]
}

export interface Card {
  suit: string
  label: string
  image: string
  image3d: string
  elements: Element[]
  meanings: {
    upright: Meaning
    reversed: Meaning
  }
}
