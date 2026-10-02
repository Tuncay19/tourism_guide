import { Redirect } from "expo-router";

// Google-dan qayıdış ünvanı buraya düşərsə, "səhifə tapılmadı" göstərməmək üçün
// sadəcə əsas səhifəyə yönləndiririk.
export default function OAuthSuccess() {
  return <Redirect href="/" />;
}
