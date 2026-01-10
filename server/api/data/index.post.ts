import type { Card } from '#shared/types/tarot'

export default defineEventHandler(async (event) => {
  const { data } = await readBody<{ data: Card[] }>(event)

  return blob.put('data.json', JSON.stringify(data ?? []))
})
