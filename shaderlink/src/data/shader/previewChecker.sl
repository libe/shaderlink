surface
previewChecker( float frequency = 5;
                 color firstColor = color(0.9, 0.9, 0.1);
				 color secondColor = color(.9, 0.1, 0.1);
                 float Ka = 1.0, Kd = 0.5, Ks = 1.0;
                 float roughness = 0.05;
                 color specularcolor = 1.0;
				 float flat = 1.0;)
{

	/*
	 * 'smod' and 'tmod' both vary from 0.0 to 1.0 'frequency' number
	 * of times over the surface in both the 's' and 't' directions.
	 * Note that the shader assumes that 's' and 't' both vary from
	 * 0.0 to 1.0 over the entire surface.
	 */
	float smod = mod(s*frequency, 1);
	float tmod = mod(t*frequency, 1);


	/*
	 * Find the current checkerboard color 'Cc'.
	 */
	color Cc;
	if (smod < 0.5) {
		if (tmod < 0.5) Cc = firstColor;
		else            Cc = secondColor;
	} else {
		if (tmod < 0.5) Cc = secondColor;
		else            Cc = firstColor;
	}


	/*
	 * Find the forward facing normal vector 'Nf'. This is used instead of
	 * simply the normal vector, since reflections do not occur from the
	 * back of a surface.
	 * Also find the incident ray direction 'IN'.
	 */
	normal Nf = faceforward(normalize(N), I);
	vector IN = normalize(I);

	/*
	 * Put all the components together.
	 */
	if (flat == 1.0) 
		Ci = Cc; 
	else
		Ci = Cc * (Ka*ambient() + Kd*diffuse(Nf)) +
		     specularcolor * (Ks*specular(Nf, -IN, roughness));

	Oi = Os;
	Ci *= Oi;
}