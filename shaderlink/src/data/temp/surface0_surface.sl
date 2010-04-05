surface surface0_surface()
{
// START NODE s0 

float s0_s = s;
// END NODE s0 

// START NODE t0 

float t0_t = t;
// END NODE t0 

// START NODE noiseST0 
float noiseST0_freq = 70.000;

float noiseST0_noise = noise(noiseST0_freq* s0_s, noiseST0_freq* t0_t);
// END NODE noiseST0 

// START NODE blinn0 
color blinn0_SurfaceColor = color(0.000,0.500,1.000);
color blinn0_ambientColor = color(0.000,0.000,0.000);
color blinn0_incandescence = color(0.000,0.000,0.000);
float blinn0_translucence = 0.000;
color blinn0_specularColor = color(0.500,0.500,0.500);
float blinn0_eccentricity = 0.300;
float blinn0_specularRollOff = 0.700;

 normal blinn0_Nf;
 vector blinn0_H, blinn0_Ln, blinn0_V;
 color blinn0_Ia, blinn0_Id, blinn0_Itr, blinn0_Is;
 float blinn0_NH, blinn0_NH2, blinn0_NHSQ, blinn0_Dd, blinn0_Gg, blinn0_VN, blinn0_VH, blinn0_LN, blinn0_Ff, blinn0_tmp;
 float blinn0_E= 1 / (blinn0_eccentricity * blinn0_eccentricity- 1);
  
 blinn0_Nf= faceforward(normalize(N), I);
 blinn0_Ia= ambient() + blinn0_ambientColor;
 blinn0_Id= noiseST0_noise* diffuse(blinn0_Nf);
 
 blinn0_Itr= 0;
 if (blinn0_translucence!= 0) {
  illuminance(P, blinn0_Nf, PI)
  blinn0_Itr+= Cl;
  blinn0_Itr*= blinn0_translucence;
 }
 
 blinn0_Is= 0;
 blinn0_V= normalize(-I);
 blinn0_VN= blinn0_V.blinn0_Nf;
 illuminance(P, blinn0_Nf, PI * 0.5) {
  blinn0_Ln= normalize(L);
  blinn0_H= normalize(blinn0_Ln+blinn0_V);
  blinn0_NH= blinn0_Nf.blinn0_H;
  blinn0_NHSQ= blinn0_NH*blinn0_NH;
  blinn0_NH2= blinn0_NH* 2;
  blinn0_Dd= (blinn0_E+1) / (blinn0_NHSQ+ blinn0_E);
  blinn0_Dd*= blinn0_Dd;
  blinn0_VH= blinn0_V.blinn0_H;
  blinn0_LN= blinn0_Ln.blinn0_Nf;
  if (blinn0_VN < blinn0_LN) {
   if (blinn0_VN* blinn0_NH2 < blinn0_VH)
   blinn0_Gg= blinn0_NH2/ blinn0_VH;
   else
   blinn0_Gg= 1 / blinn0_VN;
   }
  else {
   if (blinn0_LN* blinn0_NH2 < blinn0_VH)
   blinn0_Gg= (blinn0_LN* blinn0_NH2) / (blinn0_VH* blinn0_VN);
  else
  blinn0_Gg= 1 / blinn0_VN;
 }
 blinn0_tmp= pow((1 - blinn0_VH), 3);
 blinn0_Ff= blinn0_tmp+ (1 - blinn0_tmp) * blinn0_specularRollOff;
 blinn0_Is+= Cl * blinn0_Dd* blinn0_Gg* blinn0_Ff;
 }
 blinn0_Is*= blinn0_specularColor;
 
 color blinn0_outColor= blinn0_SurfaceColor* (blinn0_Ia + blinn0_Id + blinn0_Itr + blinn0_incandescence+ blinn0_Is);
// END NODE blinn0 

// START NODE colorToFloat0 

float colorToFloat0_outFloat = (comp(blinn0_outColor, 0) + comp(blinn0_outColor, 1) + comp(blinn0_outColor, 2)) / 3;
// END NODE colorToFloat0 

// START NODE grid1 
float grid1_freq = 75.000;
float grid1_rotation = 0.000;
float grid1_fuzz = 0.400;
color grid1_SurfaceColor = color(1.000,1.000,1.000);
color grid1_GridColor = color(0.000,0.000,0.000);

#define repeat(x,freq)    (mod((x) * (freq), 1.0))
#define pulse(a,b,fuzz,x) (smoothstep((a)-(fuzz),(a),(x)) - smoothstep((b)-(fuzz),(b),(x)))
#define rotate2d(x,y,rad,ox,oy,rx,ry) rx = ((x) - (ox)) * cos(rad) - ((y) - (oy)) * sin(rad) + (ox); ry = ((x) - (ox)) * sin(rad) + ((y) - (oy)) * cos(rad) + (oy)
#define blend(a,b,x) ((a) * (1 - (x)) + (b) * (x))

  float grid1_ss, grid1_tt;
  
  rotate2d(s, t, radians(grid1_rotation), 0.5, 0.5, grid1_ss, grid1_tt);
  grid1_ss= repeat(grid1_ss, grid1_freq);
  grid1_tt= repeat(grid1_tt, grid1_freq);

  color grid1_layer_opac= pulse(colorToFloat0_outFloat, 1-colorToFloat0_outFloat, grid1_fuzz, grid1_tt);
  color grid1_outColor = blend(grid1_SurfaceColor, grid1_GridColor, grid1_layer_opac);
// END NODE grid1 

// START NODE grid0 
float grid0_freq = 75.000;
float grid0_rotation = 45.000;
float grid0_fuzz = 0.400;
color grid0_SurfaceColor = color(1.000,1.000,1.000);
color grid0_GridColor = color(0.000,0.000,0.000);

#define repeat(x,freq)    (mod((x) * (freq), 1.0))
#define pulse(a,b,fuzz,x) (smoothstep((a)-(fuzz),(a),(x)) - smoothstep((b)-(fuzz),(b),(x)))
#define rotate2d(x,y,rad,ox,oy,rx,ry) rx = ((x) - (ox)) * cos(rad) - ((y) - (oy)) * sin(rad) + (ox); ry = ((x) - (ox)) * sin(rad) + ((y) - (oy)) * cos(rad) + (oy)
#define blend(a,b,x) ((a) * (1 - (x)) + (b) * (x))

  float grid0_ss, grid0_tt;
  
  rotate2d(s, t, radians(grid0_rotation), 0.5, 0.5, grid0_ss, grid0_tt);
  grid0_ss= repeat(grid0_ss, grid0_freq);
  grid0_tt= repeat(grid0_tt, grid0_freq);

  color grid0_layer_opac= pulse(colorToFloat0_outFloat, 1-colorToFloat0_outFloat, grid0_fuzz, grid0_tt);
  color grid0_outColor = blend(grid0_SurfaceColor, grid0_GridColor, grid0_layer_opac);
// END NODE grid0 

// START NODE mulC0 

color mulC0_outColor = grid0_outColor * grid1_outColor;
// END NODE mulC0 

// START NODE surface0 
color surface0_Oi = color(1.000,1.000,1.000);

Ci = mulC0_outColor; Oi = surface0_Oi;
// END NODE surface0 

}
