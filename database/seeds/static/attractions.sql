INSERT INTO attractions 
(att_name, att_type, is_vr_capable, att_description, height_limit_cm, capacity_per_attraction) 
VALUES
('Hyperion', 'roller_coaster', TRUE, 'Mega coaster with extreme drops and high speed.', 140, 24),
('Zadra', 'roller_coaster', TRUE, 'Wooden-steel hybrid coaster with intense inversions.', 140, 28),
('Mayang', 'roller_coaster', FALSE, 'Family-friendly coaster with smooth turns.', 120, 20),
('Dragon Zone', 'roller_coaster', FALSE, 'Suspended coaster with sharp turns and loops.', 130, 22),
('Speed Loop', 'roller_coaster', FALSE, 'High-speed coaster featuring vertical loops.', 140, 24),
('Thunderbolt', 'roller_coaster', TRUE, 'Launch coaster with rapid acceleration.', 140, 20),
('Night Fury', 'roller_coaster', TRUE, 'Indoor coaster with lighting effects.', 130, 18),
('Steel Vortex', 'roller_coaster', TRUE, 'Compact coaster with multiple inversions.', 135, 20),
('Wild Eagle', 'roller_coaster', FALSE, 'Wing coaster with near-miss elements.', 140, 28),
('Family Dragon', 'roller_coaster', TRUE, 'Gentle coaster designed for families and kids.', 100, 16),

('Splash River', 'water_ride', FALSE, 'Water flume ride with big splash ending.', 110, 20),
('Tsunami Drop', 'water_ride', FALSE, 'Tall water drop for thrill seekers.', 130, 16),
('Lazy River', 'water_ride', FALSE, 'Relaxing floating river attraction.', 0, 40),
('Aqua Coaster', 'water_ride', FALSE, 'Hybrid water and coaster experience.', 120, 18),

('VR Galaxy', 'vr_ride', TRUE, 'Virtual reality space adventure.', 120, 8),
('VR Extreme', 'vr_ride', TRUE, 'Intense VR simulation with motion seats.', 130, 6),
('VR Horror House', 'vr_ride', TRUE, 'Immersive horror VR experience.', 140, 6),

('Magic Carousel', 'family_ride', FALSE, 'Classic carousel for all ages.', 0, 30),
('Flying Elephants', 'family_ride', FALSE, 'Rotating ride for younger guests.', 90, 20),
('Mini Cars', 'kids_ride', FALSE, 'Driving attraction for children.', 80, 15),
('Pirate Ship', 'family_ride', FALSE, 'Swinging ship ride.', 110, 40),
('Tea Cups', 'family_ride', FALSE, 'Spinning cups ride.', 0, 24),

('Drop Tower', 'thrill_ride', TRUE, 'Vertical free-fall experience.', 140, 16),
('Giant Frisbee', 'thrill_ride', TRUE, 'Swinging disc ride with high G-forces.', 140, 32),
('Sky Swing', 'thrill_ride', TRUE, 'Massive swing ride with panoramic views.', 140, 20),
('Space Shot', 'thrill_ride', TRUE, 'Vertical launch ride.', 140, 12),

('Haunted Mansion', 'dark_ride', TRUE, 'Spooky indoor ride with special effects.', 100, 20),
('Observation Wheel', 'ferris_wheel', FALSE, 'Large observation wheel.', 0, 60),
('Bumper Cars', 'family_ride', FALSE, 'Classic bumper car attraction.', 110, 24);
