export default defineEventHandler((event) => {
  return blob.serve(event, 'data.json')
})
