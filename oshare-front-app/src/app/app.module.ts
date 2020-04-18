import { PostImageService } from './_services/post-image.service';
import { UserService } from './_services/user.service';
import { NewPostComponent } from './new-post/new-post.component';
import { CheckoutService } from './_services/checkout.service';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { HeaderComponent } from './shared/header/header.component';
import { SearchBarComponent } from './shared/search-bar/search-bar.component';
import { ProfileComponent } from './profile/profile.component';
import { ProductComponent } from './product/product.component';
import { ProfileHeaderComponent } from './profile/profile-header/profile-header.component';
import { PostListComponent } from './shared/post-list/post-list.component';
import { ProductListComponent } from './shared/product-list/product-list.component';
import { ProductItemComponent } from './shared/product-list/product-item/product-item.component';
import { ProductDetailComponent } from './product/product-detail/product-detail.component';
import { ReviewListComponent } from './product/review-list/review-list.component';
import { PostItemComponent } from './shared/post-list/post-item/post-item.component';
import { HomeSearchComponent } from './home-search/home-search.component';
import { SearchResultComponent } from './search-result/search-result.component';
import { CartComponent } from './cart/cart.component';
import { ProductCountListComponent } from './cart/product-count-list/product-count-list.component';
import { ProductCountItemComponent } from './cart/product-count-item/product-count-item.component';
import { CheckoutComponent } from './checkout/checkout.component';
import { PostComponent } from './post/post-page.component';
import { PostDetailComponent } from './post/post-detail/post-detail.component';
import { RegisterComponent } from './register/register.component';
import { CartService } from './_services/cart.service';
import { PostService } from './_services/post.service';
import { HttpClientModule } from '@angular/common/http';
import { ProfilePostListComponent } from './profile/profile-post-list/profile-post-list.component';
import { OrderHistoryComponent } from './order-history/order-history.component';
import { OrderProductListComponent } from './order-history/order-product-list/order-product-list.component';
import { AddReviewComponent } from "./add-review/add-review.component";
import { FacebookModule } from 'ngx-facebook';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { GlobalStreamComponent } from './global-stream/global-stream.component';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatGoogleMapsAutocompleteModule } from '@angular-material-extensions/google-maps-autocomplete';
import { AgmCoreModule } from '@agm/core';
import { AccountPageComponent } from './account-page/account-page.component';
import { MatTabsModule } from '@angular/material/tabs';

const appRoutes: Routes = [
  { path: '', component: HomeSearchComponent },
  { path: 'login', component: HomeSearchComponent },
  { path: 'post-list', component: PostListComponent },
  { path: 'post-item', component: PostItemComponent },
  { path: 'search', component: HomeSearchComponent },
  { path: 'search-result', component: SearchResultComponent },
  { path: 'post/:id', component: PostComponent },
  { path: 'product', component: ProductComponent },
  { path: 'product-list', component: ProductListComponent },
  { path: 'cart', component: CartComponent },
  { path: 'checkout', component: CheckoutComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'new-post', component: NewPostComponent },
  { path: 'add-review', component: AddReviewComponent },
  { path: 'global-stream', component: GlobalStreamComponent },
  { path: 'account', component: AccountPageComponent }
];

@NgModule({
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  declarations: [
    AppComponent,
    HeaderComponent,
    SearchBarComponent,
    // LoginComponent,
    ProfileComponent,
    ProductComponent,
    ProfileHeaderComponent,
    PostListComponent,
    ProductListComponent,
    ProductItemComponent,
    ProductDetailComponent,
    ReviewListComponent,
    PostItemComponent,
    HomeSearchComponent,
    SearchResultComponent,
    CartComponent,
    ProductCountListComponent,
    ProductCountItemComponent,
    CheckoutComponent,
    PostComponent,
    PostDetailComponent,
    RegisterComponent,
    NewPostComponent,
    ProfilePostListComponent,
    OrderHistoryComponent,
    OrderProductListComponent,
    AddReviewComponent,
    GlobalStreamComponent,
    AccountPageComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule.forRoot(appRoutes),
    ReactiveFormsModule,
    HttpClientModule,
    FacebookModule.forRoot(),
    BrowserAnimationsModule,
    ScrollingModule,
    MatGoogleMapsAutocompleteModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyC73BtQ0PBboPi_JlWKRc22qy1lq-OqDko',
      libraries: ['places']
    }),
    MatTabsModule

  ],
  exports: [
    MatTabsModule,
  ],
  providers: [
    CartService,
    CheckoutService,
    UserService,
    PostImageService,
    PostService],
  bootstrap: [AppComponent]
})
export class AppModule { }
