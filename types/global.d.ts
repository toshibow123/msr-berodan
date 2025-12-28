// DMM広告ウィジェットの型定義
declare global {
  interface Window {
    DMM?: {
      widget?: {
        init: () => void
      }
    }
  }
}

export {}

