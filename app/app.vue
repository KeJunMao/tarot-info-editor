<script setup>
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'zh-CN'
  }
})

const title = '塔罗牌信息编辑器 - Tarot Info Editor'
const description = '一个用于编辑和管理塔罗牌信息的工具。'

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description
})
const {
  cards,
  selectedCardIndex
} = useTarotCards()

const open = ref(false)
</script>

<template>
  <UApp>
    <UHeader v-model:open="open">
      <template #left>
        <NuxtLink to="/">
          <AppLogo class="w-auto h-6 shrink-0" />
        </NuxtLink>
      </template>

      <template #right>
        <UColorModeButton />
      </template>

      <template #body>
        <UNavigationMenu
          class="-mx-2.5"
          orientation="vertical"
          :items="cards.map((card, index) => {
            return {
              label: card.label,
              badge: card.suit,
              active: selectedCardIndex === index,
              onSelect: () => {
                selectedCardIndex = index
                open = false
              }
            }
          })"
        />
      </template>
    </UHeader>

    <UMain>
      <NuxtPage />
    </UMain>

    <USeparator icon="i-simple-icons-nuxtdotjs" />

    <UFooter>
      <template #left>
        <p class="text-sm text-muted">
          Built with Nuxt UI • © {{ new Date().getFullYear() }}
        </p>
      </template>
    </UFooter>
  </UApp>
</template>
