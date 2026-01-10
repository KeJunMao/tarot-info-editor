import type { Card } from '#shared/types/tarot'

export default defineEventHandler(async (event) => {
  const { index, card } = await readBody<{ index: number, card: Card }>(event)

  if (typeof index !== 'number' || !card) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Invalid payload'
    })
  }

  // Read current data
  let cards: Card[] = []
  try {
    const file = await blob.get('data.json')
    if (file) {
      const text = await file.text()
      cards = JSON.parse(text)
    }
  } catch (err) {
    console.error('Failed to read data.json', err)
  }

  if (!Array.isArray(cards)) {
    cards = []
  }

  // Update specific card
  cards[index] = card

  // Write back
  return blob.put('data.json', JSON.stringify(cards))
})
