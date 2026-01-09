export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  return blob.put('data.json', JSON.stringify(body?.data ?? []))
})
