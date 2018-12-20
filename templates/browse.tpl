<h1>Browse your favorite TV show</h1>
<div class="browse">
% for show in result:
    <article class="clickable shadowed" onclick="Browse.loadShow('{{show['id']}}')">
        <div class="rating">
            % if show['rating']:
                <i class="fas fa-star"></i><span class="average">{{show['rating']['average']}}</span>
            % end
        </div>
        <div class="cover-holder">
            <!--added by Tal-->
            % if show['image']:
                <img src="{{show['image']['original']}}" class="show-cover"/>
            % else:
                <img src="./images/404.jpg" class="show-cover"/>
            % end
        </div>
        <h3 class="show-name">{{show['name']}}</h3>
    </article>
% end
</div>